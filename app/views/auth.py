import asyncpg

from sanic import Blueprint
from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic.exceptions import ServerError
from sanic_jwt_extended import (
    refresh_jwt_required,
    jwt_required,
)
from sanic_jwt_extended.tokens import Token

from app import JWT
from app.services.user import get_user_by_email, get_user_by_id, create_user
from app.utils import JsonResponse, set_access_cookies, set_refresh_cookies
from app.decorators import expect_body
from app.models import UserModel
from app.vendors.sanic_oauth import GoogleClient, FacebookClient, NaverClient

blueprint = Blueprint("auth_blueprint", url_prefix="/auth")


@blueprint.route("/register", methods=["POST"])
@expect_body(
    email=(str, ...), password=(str, ...), nickname=(str, None), is_admin=(bool, False)
)
async def register(request: Request):
    """ register user """

    try:
        user = await create_user(**request.json)
    except asyncpg.exceptions.UniqueViolationError:
        raise ServerError("Already Registered", status_code=400)

    access_token = JWT.create_access_token(identity=str(user.id))
    refresh_token = JWT.create_refresh_token(identity=str(user.id))
    resp = JsonResponse({"new": True, "user": UserModel.from_orm(user)}, status=201,)
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp


@blueprint.route("/obtain-token", methods=["POST"])
async def obtain_token(request: Request):
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = await get_user_by_email(email)

    if user is None:
        raise ServerError("User not found.", status_code=404)

    if not user.check_password(password):
        raise ServerError("Password is wrong.", status_code=400)

    access_token = JWT.create_access_token(identity=str(user.id))
    refresh_token = JWT.create_refresh_token(identity=str(user.id))
    resp = JsonResponse({"new": False, "user": UserModel.from_orm(user)}, status=201)
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp


def get_client(request, provider: str):
    app = request.app
    if provider == "google":
        client = GoogleClient(
            request.app.async_session,
            client_id=app.config["GOOGLE_CLIENT_ID"],
            client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        )
    elif provider == "facebook":
        client = FacebookClient(
            request.app.async_session,
            client_id=app.config["FB_CLIENT_ID"],
            client_secret=app.config["FB_CLIENT_SECRET"],
        )
    elif provider == "naver":
        client = NaverClient(
            request.app.async_session,
            client_id=app.config["NAVER_CLIENT_ID"],
            client_secret=app.config["NAVER_CLIENT_SECRET"],
        )
    else:
        raise ServerError("Unknown Provider", status_code=400)
    return client


@blueprint.route("/obtain-token/<provider:string>", methods=["POST"])
async def oauth_obtain_token(request: Request, provider: str):
    client = get_client(request, provider)
    await client.get_access_token(
        request.json.get("code"), redirect_uri=request.json.get("redirectUri")
    )
    user_info, _ = await client.user_info()
    user = await get_user_by_email(user_info.email)
    if user is None:
        user = await create_user(email=user_info.email, photo=user_info.picture)
        is_new = True
    else:
        is_new = False
    access_token = JWT.create_access_token(identity=str(user.id))
    refresh_token = JWT.create_refresh_token(identity=str(user.id))
    resp = JsonResponse({"new": is_new, "user": UserModel.from_orm(user)}, status=201)
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp


@blueprint.route("/reset-password", methods=["PUT"])
@jwt_required
@expect_body(original_password=(str, ...), new_password=(str, ...))
async def reset_password(request: Request, token: Token):
    original_password = request.json.get("original_password")
    new_password = request.json.get("new_password")
    user_id = token.identity

    user = await get_user_by_id(user_id)

    if user is None:
        raise ServerError("User not found.", status_code=404)

    if user.check_password(original_password):
        user.set_password(new_password)
        await user.update(password_hash=user.password_hash).apply()
    else:
        raise ServerError("Password is wrong.", status_code=400)
    return JsonResponse({"message": "Password successfully updated"}, status=202)


@blueprint.route("/refresh-token", methods=["POST"])
@refresh_jwt_required
async def refresh_token(request, token: Token):
    """ refresh access token """
    access_token = JWT.create_access_token(identity=token.identity)
    refresh_token = JWT.create_refresh_token(identity=token.identity)
    user_id = token.identity
    user = await get_user_by_id(user_id)
    resp = JsonResponse({"new": False, "user": UserModel.from_orm(user)}, status=201)
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp


class UserProfileView(HTTPMethodView):
    @jwt_required
    async def get(self, request, token: Token):
        user_id = token.identity
        user = await get_user_by_id(user_id)
        return JsonResponse(UserModel.from_orm(user), status=200)

    @jwt_required
    async def put(self, request: Request, token: Token):
        user_id = token.identity
        data = {key: value for key, value in request.json.items()}
        user = await get_user_by_id(user_id)
        await user.update(**data).apply()
        return JsonResponse(UserModel.from_orm(user), status=202)

    async def delete(self):
        raise ServerError(status_code=405)


blueprint.add_route(UserProfileView.as_view(), "/profile")

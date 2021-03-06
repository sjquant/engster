import os
import datetime

ENV = os.getenv("ENV")
DEBUG = False if ENV == "production" else True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_URL = os.getenv("MEDIA_URL")

# Cors
CORS_ORIGINS = os.getenv("CORS", "*").split(",")
CORS_AUTOMATIC_OPTIONS = True
CORS_SUPPORTS_CREDENTIALS = True

# DB
DB_PORT = os.getenv("DB_PORT", "5123")
DB_DATABASE = os.getenv("DB_NAME", "engster")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_URL = f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

# JWT

csrf_protect = os.getenv("JWT_CSRF_PROTECT", "false")
cookie_secure = os.getenv("JWT_COOKIE_SECURE", "false")

if csrf_protect.lower() == "true":
    csrf_protect = True
else:
    csrf_protect = False

if cookie_secure.lower() == "true":
    cookie_secure = True
else:
    cookie_secure = False

JWT = {
    "namespace": "https://engster.co.kr",
    "private_claim_prefix": "engster_private",
    "secret_key": os.getenv("JWT_SECRET_KEY", "secret_key"),
    "token_location": ("cookies",),
    "access_token_expires": datetime.timedelta(
        seconds=int(os.getenv("JWT_ACCESS_EXPIRES", "86400"))
    ),
    "refresh_token_expires": datetime.timedelta(
        seconds=int(os.getenv("JWT_REFRESH_EXPIRES", "2419200"))
    ),
    "csrf_protect": csrf_protect,
    "jwt_csrf_header": "X-CSRF-Token",
    "refresh_jwt_csrf_header": "X-RCSRF-Token",
    "cookie_secure": cookie_secure,
    "cookie_domain": os.getenv("JWT_COOKIE_DOMAIN", None),
    "default_iss": "engster.co.kr",
}

# Social Auth
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
FB_CLIENT_ID = os.getenv("FB_CLIENT_ID")
FB_CLIENT_SECRET = os.getenv("FB_CLIENT_SECRET")
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "engster.noreply@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_SMTP_HOST = os.getenv("EMAIL_SMTP_HOST", "127.0.0.1")
EMAIL_SMTP_PORT = os.getenv("EMAIL_SMTP_PORT", 1025)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

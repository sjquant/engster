from app import db
from app.models import BaseModel


class Content(BaseModel):

    __tablename__ = 'content'

    id = db.Column(db.Integer, db.Sequence('content_id_seq'), primary_key=True)
    title = db.Column(db.String(255))
    year = db.Column(db.String(4), nullable=False)
    reference = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    def __repr__(self):
        return '<Content {}>'.format(self.title)


class Category(BaseModel):

    __tablename__ = 'category'

    id = db.Column(db.Integer, db.Sequence(
        'category_id_seq'), primary_key=True)
    category = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Category {}>'.format(self.category)


class Genre(BaseModel):

    __tablename__ = 'genre'

    id = db.Column(db.Integer, db.Sequence('content_id_seq'), primary_key=True)
    genre = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Genre {}>'.format(self.genre)


class Content_Genre(BaseModel):

    __tablename__ = 'content_genre'

    id = db.Column(db.Integer, db.Sequence(
        'content_genre_id_seq'), primary_key=True),
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))

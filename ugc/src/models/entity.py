from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4


db = SQLAlchemy()

class Like(db.Model):
    """Модель для лайков пользователей."""
    __tablename__ = 'likes'

    user_id = db.Column(db.String, nullable=False)
    movie_id = db.Column(db.String, nullable=False)

    __table_args__ = (db.PrimaryKeyConstraint('user_id', 'movie_id'),)


class Comment(db.Model):
    """Модель для пользовательских комментариев."""
    __tablename__ = 'comments'

    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    movie_id = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, user_id, movie_id, content):
        self.id = str(uuid4())
        self.user_id = user_id
        self.movie_id = movie_id
        self.content = content


class Favourite(db.Model):
    """Модель для избранных фильмов пользователя."""
    __tablename__ = "favourites"

    user_id = db.Column(db.String, nullable=False)
    movie_id = db.Column(db.String, nullable=False)

    __table_args__ = (db.PrimaryKeyConstraint('user_id', 'movie_id'),)

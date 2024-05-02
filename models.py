"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


dt = datetime.now()

truncated_datetime = f"{dt.year}-{dt.month}-{dt.day} {dt.hour}:{dt.minute}:{dt.second}"


class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String, nullable=False)

    last_name = db.Column(db.String, nullable=False)

    image_url = db.Column(
        db.String,
        default="https://images.unsplash.com/photo-1511367461989-f85a21fda167?q=80&w=1631&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    )


class Post(db.Model):
    """Posts made by user to be saved to the database."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String, nullable=False, unique=True)

    content = db.Column(db.String)

    created_at = db.Column(db.DateTime, default=truncated_datetime)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("User", backref="posts")

    assignments = db.relationship("PostTag", cascade="all,delete", backref="post")

    tags = db.relationship("Tag", secondary="posts_tags", backref="posts")


class Tag(db.Model):
    """Tags made by user to be added to posts."""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String, unique=True, nullable=False)

    assignments = db.relationship("PostTag", cascade="all,delete", backref="tag")


class PostTag(db.Model):
    """Table that joins post and tag."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)

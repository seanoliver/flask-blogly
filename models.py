from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
import os
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///flask_blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy()

DEFAULT_IMG = 'https://picsum.photos/100'



def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model."""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    first_name = db.Column(
        db.String(50),
        nullable=False)

    last_name = db.Column(
        db.String(50),
        nullable=False)

    image_url = db.Column(
        db.Text,
        default = DEFAULT_IMG,
        nullable=True)

    posts = db.relationship(
        'Post',
        backref='users'         # FIXME: Change to 'user'
    )

class Post(db.Model):
    """Post model."""

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    title = db.Column(
        db.String(50),
        nullable=False)

    content = db.Column(
        db.Text,
        nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default = db.func.now(),
        nullable=False)

    # TODO: user backref

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id') # FIXME: add not nullable
    )

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


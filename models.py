from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

"""Models for Blogly."""
class User(db.Model):
    __tablename__= "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    image_url = db.Column(db.String)

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(50), nullable = False)
    content = db.Column(db.String(250), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='posts')
    tags = db.relationship('Tag', secondary = 'posttag', backref = 'post' )

class Tag(db.Model):
    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(50), nullable = False, unique = True)
    posts = db.relationship('Post', secondary = 'posttag', backref = 'tag')

class PostTag(db.Model):
    __tablename__ = "posttag"
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key = True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key = True)
    tag = db.relationship('Tag')
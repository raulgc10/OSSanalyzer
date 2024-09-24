from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_name = db.Column(db.String(100))
    repository_name = db.Column(db.String(100))
    usernames = db.Column(db.JSON)
    repo_data = db.Column(db.JSON)
    lg_percent = db.Column(db.JSON)
    num_files = db.Column(db.Integer)
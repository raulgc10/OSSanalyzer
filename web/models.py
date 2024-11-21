from . import db
from flask_login import UserMixin

class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_name = db.Column(db.String(100))
    repository_name = db.Column(db.String(100))
    usernames = db.Column(db.JSON)
    repo_data = db.Column(db.JSON)
    lg_percent = db.Column(db.JSON)
    num_files = db.Column(db.Integer)
    min_languages = db.Column(db.JSON)
    default_branch = db.Column(db.String(100))
    last_commit = db.Column(db.String(100))
    total_commits_on_min_languages = db.Column(db.JSON)
    min_languages_experts = db.Column(db.JSON)

class UserExpertise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    repositories_contribution = db.Column(db.JSON)
    commits_min_languages_per_repo = db.Column(db.JSON)

class Languages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lan_name = db.Column(db.String(100))
    lan_num_users = db.Column(db.Integer)
    lan_users = db.Column(db.JSON)
    lan_num_commits = db.Column(db.Integer)
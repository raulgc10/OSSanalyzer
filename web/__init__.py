from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
DB_NAME = "database.db"
basedir = os.path.abspath(os.path.dirname(__file__))
# Función para crear la app y registrar los endpoints disponibles
def create_app():
    app = Flask (__name__)
    app.secret_key = "tsiñhp,rxvsmysfpt@h,soñ-vp," 
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'database.db')
    db.init_app(app)

    from .endpoints import endpoint
    from .authentication import auth

    app.register_blueprint(endpoint, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Repository

    with app.app_context():
        db.create_all()

    return app

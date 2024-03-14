from flask import Flask

# Función para crear la app y registrar los endpoints disponibles
def create_app():
    app = Flask (__name__)

    from .endpoints import endpoint
    from .authentication import auth

    app.register_blueprint(endpoint, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    return app
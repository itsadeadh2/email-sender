import os
from flask import Flask
from flask_smorest import Api

from src.resources import email_bp, health_bp


def create_app():
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["TABLE_NAME"] = os.getenv("TABLE_NAME")
    app.config["QUEUE_URL"] = os.getenv("QUEUE_URL")

    api = Api(app)

    api.register_blueprint(email_bp)
    api.register_blueprint(health_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='localhost', port=5000)
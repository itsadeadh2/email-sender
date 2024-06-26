# app.py
from flask import Flask, request
from flask_smorest import Api
from flask_smorest import Blueprint
from flask.views import MethodView
from src.services import QueueService, EmailDAL, Handler, Validators

def create_app():
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    api = Api(app)


    blp = Blueprint("email", "email", description="Operations on emails")
    @blp.route('/email')
    class Email(MethodView):
        def __init__(self):
            self.handler = Handler(
                validators=Validators,
                email_dal=EmailDAL(),
                queue_service=QueueService()
            )

        def post(self):
            body = request.get_json()
            data, status = self.handler.handle(body)
            return data, status

        def get(self):
            print("test")
            return {"emails": []}, 200

    api.register_blueprint(blp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='localhost', port=3000)
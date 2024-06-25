# app.py
from flask import Flask, request
from flask_smorest import Api
from flask_smorest import Blueprint
from flask.views import MethodView
from services import QueueService, EmailDAL, Handler, Validators

app = Flask(__name__)

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
        return {"emails": []}, 200



api.register_blueprint(blp)
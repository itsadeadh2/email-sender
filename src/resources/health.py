from flask_smorest import Blueprint
from flask.views import MethodView

bp = Blueprint("health", "health", description="Healthcheck operations")


@bp.route('/health')
class Health(MethodView):
    def get(self):
        print("test")
        return {}, 200


from src.app import app  # Assuming your Flask app is in app.py
import serverless_wsgi


def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)

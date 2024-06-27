from unittest import TestCase
from src.app import create_app


class BaseTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"

    def setUp(self):
        app = create_app()
        self.app = app.test_client()
        self.app_context = app.app_context

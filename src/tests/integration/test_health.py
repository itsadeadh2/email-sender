from src.tests.integration.base_test import BaseTest


class TestHealth(BaseTest):

    def test_health(self):
        res = self.app.get('/health')
        self.assertEqual(res.status_code, 200)

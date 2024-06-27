import unittest
from unittest.mock import Mock
from src.handlers import EmailHandler
from src.exc import InvalidEmailError, PersistenceError, QueueInteractionError


class TestEmailHandler(unittest.TestCase):
    def setUp(self):
        self.validators = Mock()
        self.email = Mock()
        self.queue = Mock()
        self.handler = EmailHandler(
            email=self.email,
            queue=self.queue
        )

    def test_persist_email(self):
        event = {'email': 'invalidemail'}
        self.handler.handle(data=event)
        self.email.save.assert_called_once_with(event['email'])

    def test_persist_email_failure(self):
        event = {'email': 'invalidemail'}
        error_message = 'failed to save email'
        self.email.save.side_effect = PersistenceError(error_message)
        res = self.handler.handle(data=event)
        expected_res = {
            "message": error_message,
        }, 500
        self.assertEqual(expected_res, res)

    def test_send_to_queue(self):
        event = {'email': 'invalidemail'}
        self.handler.handle(data=event)
        self.queue.add_to_queue.assert_called_once_with(event['email'])

    def test_send_to_queue_failure(self):
        event = {'email': 'invalidemail'}
        error_message = 'failed to send email to queue'
        self.queue.add_to_queue.side_effect = QueueInteractionError(error_message)
        res = self.handler.handle(data=event)
        expected_res = {
            "message": error_message,
        }, 500
        self.assertEqual(expected_res, res)

    def test_success(self):
        event = {'email': 'invalidemail'}
        res = self.handler.handle(data=event)
        expected_res = {
            "message": f"Successfully received contact request. You should receive an email shortly on {event['email']} with my contact information.",
        }, 200
        self.assertEqual(expected_res, res)


if __name__ == "__main__":
    unittest.main()

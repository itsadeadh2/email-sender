import unittest
from unittest.mock import Mock
from src.main import Validators, Service
from src.exc import InvalidEmailError, PersistenceError, QueueInteractionError


class TestValidators(unittest.TestCase):
    def test_raises_on_invalid_email(self):
        invalid_emails = ['invalidemail', 'invalid.com', 'invalid@', '@invalid.com']
        for email in invalid_emails:
            with self.assertRaisesRegex(InvalidEmailError, 'The provided email is invalid'):
                Validators.validate_email(email)

    def test_no_raise_on_valid_email(self):
        email = 'test@test.com'
        raised = False
        try:
            Validators.validate_email(email)
        except:
            raised = True
        self.assertEqual(raised, False)


class TestService(unittest.TestCase):
    def setUp(self):
        self.validators = Mock()
        self.email_dal = Mock()
        self.queue_service = Mock()
        self.service = Service(
            validators=self.validators,
            email_dal=self.email_dal,
            queue_service=self.queue_service
        )

    def test_call_validators(self):
        event = {'email': 'invalidemail'}
        self.service.handle(event=event)
        self.validators.validate_email.assert_called_once_with(event['email'])

    def test_validation_failure(self):
        event = {'email': 'invalidemail'}
        error_message = 'foo'
        self.validators.validate_email.side_effect = InvalidEmailError(error_message)
        res = self.service.handle(event=event)
        expected_res = {
                "message": error_message,
                "status_code": 400
        }
        self.assertEqual(expected_res, res)

    def test_persist_email(self):
        event = {'email': 'invalidemail'}
        self.service.handle(event=event)
        self.email_dal.save.assert_called_once_with(event['email'])

    def test_persist_email_failure(self):
        event = {'email': 'invalidemail'}
        error_message = 'failed to save email'
        self.email_dal.save.side_effect = PersistenceError(error_message)
        res = self.service.handle(event=event)
        expected_res = {
            "message": error_message,
            "status_code": 500
        }
        self.assertEqual(expected_res, res)

    def test_send_to_queue(self):
        event = {'email': 'invalidemail'}
        self.service.handle(event=event)
        self.queue_service.add_to_queue.assert_called_once_with(event['email'])

    def test_send_to_queue_failure(self):
        event = {'email': 'invalidemail'}
        error_message = 'failed to send email to queue'
        self.queue_service.add_to_queue.side_effect = QueueInteractionError(error_message)
        res = self.service.handle(event=event)
        expected_res = {
            "message": error_message,
            "status_code": 500
        }
        self.assertEqual(expected_res, res)

    def test_success(self):
        event = {'email': 'invalidemail'}
        res = self.service.handle(event=event)
        expected_res = {
            "message": f"Successfully received contact request. You should receive an email shortly on {event['email']} with my contact information.",
            "status_code": 200
        }
        self.assertEqual(expected_res, res)


if __name__ == "__main__":
    unittest.main()

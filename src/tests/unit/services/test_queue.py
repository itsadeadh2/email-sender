import os
import unittest
from unittest.mock import Mock

from src.services import Queue
from src.exc import QueueInteractionError


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.sqs = Mock()
        self.queue = Queue(queue_url='', sqs=self.sqs)

    def test_add_to_queue_failure(self):
        self.sqs.send_message.side_effect = QueueInteractionError
        with self.assertRaises(QueueInteractionError):
            self.queue.add_to_queue('foo')

    def test_call_add_to_queue_with_proper_params(self):
        email = 'foo@baz.com'
        self.queue.add_to_queue(email)
        expected_call = {
            'QueueUrl': os.getenv('QUEUE_URL'),
            'MessageBody': email
        }
        self.sqs.send_message.assert_called_once_with(**expected_call)
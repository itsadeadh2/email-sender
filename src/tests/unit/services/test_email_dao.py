import unittest
from unittest.mock import Mock

from src.services import EmailDAO
from src.exc import PersistenceError


class TestEmailDAO(unittest.TestCase):
    def setUp(self):
        self.sqs = Mock()
        self.table = Mock()
        self.sqs.Table.return_value = self.table
        self.email_dao = EmailDAO(table_name='', db=self.sqs)

    def test_save_failure(self):
        self.table.put_item.side_effect = PersistenceError
        with self.assertRaises(PersistenceError):
            self.email_dao.save('foo@baz.com')

    def test_call_save_with_proper_params(self):
        email = 'foo@baz.com'
        self.email_dao.save(email)
        expected_call = {
            'Item': {
                'email': email
            }
        }
        self.table.put_item.assert_called_once_with(**expected_call)
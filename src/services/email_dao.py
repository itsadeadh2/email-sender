import boto3

from src.exc import PersistenceError
from flask import current_app


class EmailDAO:
    def __init__(self, table_name, db=None):
        self.db = db or boto3.resource('dynamodb')
        self.table = self.db.Table(table_name)

    def save(self, email):
        try:
            self.table.put_item(
                Item={
                    'email': email,
                }
            )
        except Exception as e:
            raise PersistenceError(f"There was an error when saving the email {str(e)}")
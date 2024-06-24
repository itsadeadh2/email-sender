import re
import boto3
import os
from botocore.exceptions import ClientError
from .exc import InvalidEmailError, PersistenceError, QueueInteractionError


class Validators:
    @staticmethod
    def validate_email(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.fullmatch(regex, email):
            raise InvalidEmailError("The provided email is invalid")


class EmailDAL:
    def __init__(self, db=None):
        self.db = db or boto3.resource('dynamodb')
        self.table = self.create_table()

    def create_table(self):
        try:
            table = self.db.create_table(
                TableName='EmailTable',
                KeySchema=[
                    {
                        'AttributeName': 'email',
                        'KeyType': 'HASH'  # Partition key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'email',
                        'AttributeType': 'S'  # String type
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )

            table.meta.client.get_waiter('table_exists').wait(TableName='EmailTable')
            print("Table created successfully.")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                print("Table already exists.")
        finally:
            return table

    def save(self, email):
        try:
            self.table.put_item(
                Item={
                    'email': email,
                }
            )
        except Exception as e:
            raise PersistenceError(f"There was an error when saving the email {str(e)}")


class QueueService:
    def __int__(self, sqs=None):
        self.sqs = sqs or boto3.client('sqs')
        self.queue_url = os.getenv('QUEUE_URL')

    def add_to_queue(self, email):
        try:
            self.sqs.send_message(
                QueueUrl=self.queue_url,
                MessageBody=email
            )
        except Exception as e:
            raise QueueInteractionError(f"There was an error when sending the email to the sqs queue {str(e)}")


class Service:
    def __init__(
            self,
            validators: Validators,
            email_dal: EmailDAL,
            queue_service: QueueService
    ):
        self.validators = validators
        self.email_dal = email_dal
        self.queue_service = queue_service

    def handle(self, event, context=None):
        try:
            email = event.get('email', '')
            self.validators.validate_email(email)
            self.email_dal.save(email)
            self.queue_service.add_to_queue(email)
            return {
                "message": f"Successfully received contact request. You should receive an email shortly on {email} with my contact information.",
                "status_code": 200
            }
        except InvalidEmailError as e:
            return {
                "message": str(e),
                "status_code": 400
            }
        except PersistenceError as e:
            return {
                "message": str(e),
                "status_code": 500
            }
        except QueueInteractionError as e:
            return {
                "message": str(e),
                "status_code": 500
            }


def lambda_handler(event, context):
    email_dal = EmailDAL()
    queue_service = QueueService()
    service = Service(
        validators=Validators,
        email_dal=email_dal,
        queue_service=queue_service
    )
    return service.handle(event=event, context=context)

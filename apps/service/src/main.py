import re
import boto3
import os
from exc import InvalidEmailError, PersistenceError, QueueInteractionError


class Validators:
    @staticmethod
    def validate_email(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.fullmatch(regex, email):
            raise InvalidEmailError("The provided email is invalid")


class EmailDAL:
    def __init__(self, db=None):
        self.db = db or boto3.resource('dynamodb')
        self.table = self.db.Table(os.getenv('TABLE_NAME'))

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
    def __init__(self, sqs=None):
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

import re
from apps.service.src.exc import InvalidEmailError, PersistenceError, QueueInteractionError


class Validators:
    @staticmethod
    def validate_email(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.fullmatch(regex, email):
            raise InvalidEmailError("The provided email is invalid")


class EmailDAL:
    def save(self, email):
        pass


class QueueService:
    def add_to_queue(self, email):
        pass


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
    service = Service(
        event=event,
        context=context,
        validators=Validators
    )
    return service.handle()

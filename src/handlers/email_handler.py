from src.exc import InvalidEmailError, PersistenceError, QueueInteractionError
from src.services import EmailDAO, Queue


class EmailHandler:
    def __init__(
            self,
            email: EmailDAO,
            queue: Queue
    ):
        self.email = email
        self.queue = queue

    def handle(self, data):
        try:
            email = data.get('email', '')
            self.email.save(email)
            self.queue.add_to_queue(email)
            return {
                "message": f"Successfully received contact request. You should receive an email shortly on {email} with my contact information.",
            }, 200
        except InvalidEmailError as e:
            return {
                "message": str(e)
            }, 400
        except PersistenceError as e:
            return {
                "message": str(e),
            }, 500
        except QueueInteractionError as e:
            return {
                "message": str(e),
            }, 500


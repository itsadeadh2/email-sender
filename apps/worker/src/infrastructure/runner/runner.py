from apps.worker.src.infrastructure.queue.queue import Queue
from apps.worker.src.domain import Handler
import apps.worker.src.infrastructure.exc as exc


class Runner:

    def __init__(
            self,
            queue_service: Queue,
            handler: Handler
    ):
        self.queue_service = queue_service
        self.handler = handler

    def process(self, *args, **kwargs):
        try:
            response = self.queue_service.receive_message(*args, **kwargs)
            if "Messages" in response:
                messages_list = response["Messages"]
                for message in messages_list:
                    self.handler.handle(message)
                    self.queue_service.delete_message(receipt_handle=message["ReceiptHandle"])
        except exc.InvalidEmailError as e:
            print(str(e))
            self.queue_service.delete_message(receipt_handle=message["ReceiptHandle"])
        except exc.MailingError as e:
            print('- MAILING EXCEPTION  -')
            print(str(e))
            print('Keeping message on queue to be reprocessed.')
        except Exception as e:
            print(f"There was error while processing the message: {str(e)}")

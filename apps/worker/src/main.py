import os
from dotenv import load_dotenv
import boto3


class QueueService:
    def __init__(self, sqs=None):
        self.sqs = sqs or boto3.client('sqs')
        self.queue_url = os.getenv('QUEUE_URL')

    def receive_message(self, max_number_of_messages=1, wait_time_seconds=20, visibility_timeout=60):
        response = self.sqs.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=max_number_of_messages,
            WaitTimeSeconds=wait_time_seconds,
            VisibilityTimeout=visibility_timeout,
        )
        return response

    def delete_message(self, receipt_handle):
        return self.sqs.delete_message(QueueUrl=self.queue_url, ReceiptHandle=receipt_handle)


class Runner:

    def __init__(
            self,
            queue_service: QueueService
    ):
        self.queue_service = queue_service

    def process(self, *args, **kwargs):
        try:
            response = self.queue_service(*args, **kwargs)
            if "Messages" in response:
                messages_list = response["Messages"]
                for message in messages_list:
                    email = message.get("Body")
                    print(f'Received email: f{email}')
                    self.queue_service.delete_message(receipt_handle=message["ReceiptHandle"])
        except Exception as e:
            print(f"There was an error while consuming the message: {str(e)}")


def create_runner():
    queue_service = QueueService()
    return Runner(
        queue_service=queue_service
    )


if __name__ == "__main__":
    load_dotenv()
    runner = create_runner()
    print('- WORKER STARTED -')
    print(f'Listening for messages on {runner.queue_service.queue_url}')
    while True:
        runner.process()

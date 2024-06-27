import boto3
import os

from src.exc import QueueInteractionError


class Queue:
    def __init__(self, queue_url, sqs=None):
        self.sqs = sqs or boto3.client('sqs')
        self.queue_url = os.getenv(queue_url)

    def add_to_queue(self, email):
        try:
            self.sqs.send_message(
                QueueUrl=self.queue_url,
                MessageBody=email
            )
        except Exception as e:
            raise QueueInteractionError(f"There was an error when sending the email to the sqs queue {str(e)}")
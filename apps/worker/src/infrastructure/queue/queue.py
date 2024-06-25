import os
import boto3
from dotenv import load_dotenv
load_dotenv()


class Queue:
    def __init__(self, sqs=None):
        self.sqs = sqs or boto3.client('sqs')
        self.queue_url = os.getenv('QUEUE_URL')
        if not self.queue_url:
            raise Exception("Invalid Queue URL")

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
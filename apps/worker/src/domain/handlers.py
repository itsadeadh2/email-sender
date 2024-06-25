from abc import ABC

from apps.worker.src.infrastructure.mail.mail import Mail
from apps.worker.src.infrastructure.mail.templates.parsers import ContactInfoParser
from apps.worker.src.infrastructure.validators import validate_email


class Handler(ABC):
    def handle(self, message):
        pass


class ContactInfoHandler(Handler):
    def __init__(
            self,
            mail: Mail,
    ):
        self.mail = mail

    def handle(self, message):
        email = message.get('Body')
        print(f'Received email: {str(email)}')
        validate_email(message)
        # retrieve additional information
        parser = ContactInfoParser()
        html = parser.get_html()
        text = parser.get_text()
        self.mail.send_email(
            to=email,
            subject="Contact Information - Thiago Barbosa",
            text=text,
            html=html
        )
import ssl
from email.message import EmailMessage
import smtplib
from smtplib import SMTPServerDisconnected, SMTPRecipientsRefused
from loguru import logger
from .errors import InvalidSenderEmail

class EmailSender:
    def __init__(self, email, password):
        self._sender = None
        self.email_sender = email
        self._email_password = password
        self._context = ssl.create_default_context()
        self.connect()

    def send_message(self, to, subject, body):
        em = EmailMessage()
        em["From"] = self.email_sender
        em["To"] = to
        em["Subject"] = subject
        em.set_content(body)

        try:
            self._sender.sendmail(self.email_sender, to, em.as_string())
        except SMTPServerDisconnected:
            logger.error("The server was disconnecting, trying to reconnect")
            self.connect()
        except SMTPRecipientsRefused:
            raise InvalidSenderEmail(to)

    def __del__(self):
        self._sender.close()

    def connect(self):
        self._sender = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=self._context)
        self._sender.login(self.email_sender, self._email_password)
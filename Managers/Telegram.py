import requests
from loguru import logger


class TelegramManager:
    def __init__(self, telegram_key, notification_url):
        self.api_key = telegram_key
        self.url = notification_url

    def sent_notification(self, id, subject, body):
        logger.debug(f"Sending the notification to {id}")
        requests.post(self.url, {"id": id, "title": subject, "body": body})
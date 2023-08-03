import datetime
import os

from dotenv import load_dotenv
from Managers import TelegramManager
from Clients import PostgresClient
from loguru import logger


load_dotenv()

telegram_domain = os.getenv("TELEGRAM_DOMAIN")
telegram_token = os.getenv("TELEGRAM_TOKEN")
telegram_url = (telegram_domain + "/" + telegram_token + "/" + "notify").strip()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_database = os.getenv("DB_DATABASE")


telegram_manager = TelegramManager(telegram_token, telegram_url)
db = PostgresClient(db_user, db_password, db_host, db_port, db_database)

logger.add("./logs/telegram_{time}.log", rotation="200 MB")

user_contacts = db.take_user_telegram(datetime.datetime.today())
sent_ids = []
logger.debug(f"take {len(user_contacts)} messages for sending to telegram")
for user_contact in user_contacts:
    user_id = user_contact[0]
    telegram = user_contact[1]
    subject = user_contact[2]
    body = user_contact[3]
    try:
        if telegram:
            logger.debug(f"Sending message to telegram user {telegram}")
            telegram_manager.sent_notification(telegram, subject, body)
        sent_ids.append(user_id)
    except Exception as e:
        logger.error(f"cannot send message, err= {e}")


try:
    db.set_sent_telegram(sent_ids)
except Exception as e:
    logger.error(f"cannot set is_sent flag, err= {e}")

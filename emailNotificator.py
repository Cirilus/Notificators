import datetime
import os

from dotenv import load_dotenv
from Managers import EmailSender, InvalidSenderEmail
from Clients import PostgresClient
from loguru import logger


load_dotenv()


email = os.getenv("EMAIL")
email_password = os.getenv("EMAIL_PASSWORD")

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_database = os.getenv("DB_DATABASE")


email_manager = EmailSender(email, email_password)
db = PostgresClient(db_user, db_password, db_host, db_port, db_database)


user_contacts = db.take_user_emails(datetime.datetime.today())
sent_ids = []
logger.debug(f"take {len(user_contacts)} message for sending")
for user_contact in user_contacts:
    user_id = user_contact[0]
    email = user_contact[1]
    subject = user_contact[2]
    body = user_contact[3]
    try:
        if email:
            logger.debug(f"Sending message to email {email}")
            email_manager.send_message(email, subject, body)
        sent_ids.append(user_id)
    except InvalidSenderEmail as e:
        logger.error(f"The mail is invalid, err = {e}")
        sent_ids.append(user_id)
    except Exception as e:
        logger.error(f"cannot send message, err= {e}")

try:
    db.set_sent_email(sent_ids)
except Exception as e:
    logger.error(f"cannot set is_sent flag, err= {e}")

import datetime
from typing import List

import psycopg2
from loguru import logger


class PostgresClient:
    def __init__(self, user, password, host, port="5432", database="postgres"):
        logger.debug(f"Connecting to db")
        self._connection = psycopg2.connect(user=user, password=password,
                                            host=host, port=port, database=database)
        self._cursor = self._connection.cursor()
        logger.info("Successfully connected to db")

    def take_user_telegram(self, time):
        user_contacts = []
        sql = f"SELECT n.id, COALESCE(a.telegram, n.telegram) as telegram, n.title, n.body \
            FROM notification n \
            LEFT JOIN account_notification an on n.id = an.notification_id \
            LEFT JOIN account a on a.id = an.account_id \
            WHERE n.execution < %s and n.is_sent_telegram = false;"
        try:
            self._cursor.execute(sql, [time])
            user_contacts = self._cursor.fetchall()
        except Exception as e:
            logger.error(f"Cannot take the user contacts with time {time}, err= {e}")
        return user_contacts

    def take_user_emails(self, time):
        user_contacts = []
        sql = f"SELECT n.id, COALESCE(a.email, n.email) as email, n.title, n.body \
            FROM notification n \
            LEFT JOIN account_notification an on n.id = an.notification_id \
            LEFT JOIN account a on a.id = an.account_id \
            WHERE n.execution < %s and n.is_sent_email = false;"
        try:
            self._cursor.execute(sql, [time])
            user_contacts = self._cursor.fetchall()
        except Exception as e:
            logger.error(f"Cannot take the user contacts with time {time}, err= {e}")
        return user_contacts

    def set_sent_telegram(self, ids: List[str]):
        sql = "UPDATE notification SET is_sent_telegram=true WHERE id=ANY(%s::uuid[]);"
        try:
            self._cursor.execute(sql, (ids,))
            self._connection.commit()
        except Exception as e:
            logger.error(f"Cannot set the sent check in ids {ids}, err= {e}")

    def set_sent_email(self, ids: List[str]):
        sql = "UPDATE notification SET is_sent_email=true WHERE id=ANY(%s::uuid[]);"
        try:
            self._cursor.execute(sql, (ids,))
            self._connection.commit()
        except Exception as e:
            logger.error(f"Cannot set the sent check in ids {ids}, err= {e}")
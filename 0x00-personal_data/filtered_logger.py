#!/usr/bin/env python3
"""
This module contains a method that returns the log message obfuscated
"""

import re
import logging
import os
import bcrypt
import mysql.connector


def filter_datum(fields, redaction, message, separator):
    """
    Returns the log message obfuscated
    """

    regex = '|'.join(fields)
    return re.sub(regex, redaction, message)


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    SEPARATOR = ";"

    def __init__(self, fields):
        """
        Initialize RedactingFormatter object
        """

        super(RedactingFormatter, self).__init__(
            "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
            )
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filter values in incoming log records using `filter_datum`.
        Values for fields in `self.fields` should be filtered with
        `self.redaction` and separated by `self.separator`.
        """

        message = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION, message, self.SEPARATOR
            )


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def get_logger() -> logging.Logger:
    """
    Returns a logging.Logger object with a log message
    """

    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db():
    """
    Returns a connector to the database
    """

    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    connector = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )

    return connector


def main():
    """
    Connects to the database and retrieves all rows from the users table
    """

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    [print(user) for user in cursor]

    cursor.close()
    db.close()


def hash_password(password: str) -> bytes:
    """
    Hashes the password using bcrypt
    """

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates if the provided password matches the hashed password
    """

    return bcrypt.checkpw(password.encode(), hashed_password)

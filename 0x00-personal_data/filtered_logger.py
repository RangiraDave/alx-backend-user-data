#!/usr/bin/env python3
"""
This module contains a method that returns the log message obfuscated
"""

import re
import logging


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

        super(RedactingFormatter, self).__init__("[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s")
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filter values in incoming log records using `filter_datum`.
        Values for fields in `self.fields` should be filtered with
        `self.redaction` and separated by `self.separator`.
        """

        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)

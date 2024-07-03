#!/usr/bin/env python3
"""
This module contains a method that returns the log message obfuscated
"""

import re


def filter_datum(fields, redaction, message, separator):
    regex = '|'.join(fields)
    return re.sub(regex, redaction, message)

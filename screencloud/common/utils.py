import time
import logging
from base64 import urlsafe_b64encode
from os import urandom

def get_logger(name, level=logging.DEBUG, attach_null_handler=True):
    """
    Return the logger for the given name.

    Log-level defaults to DEBUG and a null handler is attached by
    default to avoid the annoying log handler not found warnings
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if attach_null_handler:
        logger.addHandler(logging.NullHandler())
    return logger

def timestamp():
    """
    Return current unix time as a float.
    """
    return time.time()

def url_safe_token(bytelength=32):
    """
    Create a new random url-safe token.
    """
    return urlsafe_b64encode(urandom(bytelength))

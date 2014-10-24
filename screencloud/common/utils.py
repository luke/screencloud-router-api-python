import time
import logging
from base64 import urlsafe_b64encode
from os import urandom
from passlib.hash import bcrypt_sha256

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


class Connections(object):
    """
    A simple object used to pass connection data around the app.

    Expects redis to be a redis client and sql to be a sqlalchemy session.
    """
    def __init__(self, redis, sql):
        self.redis = redis
        self.sql = sql


def encrypt_secret(secret):
    """
    Generate a secure (one-way) hash from the given secret.  Suitable for storing
    passwords.

    Returns:
        The hashed secret.
    """
    return bcrypt_sha256.encrypt(secret, rounds=8)


def verify_secret(secret, hash):
    """
    Check to see if the provided secret matches the hashed value.

    Companion to `utils.encrypt_secret`

    Returns:
        Bool indicating whether or not the secret matches the hash.
    """
    return bcrypt_sha256.verify(secret, hash)

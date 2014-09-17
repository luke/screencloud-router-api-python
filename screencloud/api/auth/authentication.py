from collections import namedtuple
import uuid

from screencloud.common import utils
from screencloud.common.exceptions import AuthenticationError
from screencloud.redis import keys
from screencloud.sql import models
from . import scopes
from .. import g

#: Authentication model to pass around
Authentication = namedtuple(
    'Authentication', 
    [
        'is_anonymous',
        'scope',
        'token',
        'account',
    ]
)

def create_anonymous_token():
    """
    Generate an auth token with anonymous scope and persist (redis).

    Returns the generated token string.
    """
    token = uuid.uuid4().hex
    key = keys.authentication_token(token)
    data = {
        'scope': scopes.ANONYMOUS,
        'last_accessed': utils.timestamp(),
    }
    g.redis.hmset(key, data)
    return token


def lookup(token, update_timestamp=True):
    """
    

    Raises AuthenticationError.
    """

    # Lookup the token in redis
    key = keys.authentication_token(token)
    data = g.redis.hgetall(key)

    if not data:
        raise AuthenticationError

    if update_timestamp:
        g.redis.hset(key, 'last_accessed', utils.timestamp())

    # Return valid anonymous auth
    if data['scope'] == scopes.ANONYMOUS:
        return Authentication(
            is_anonymous=True,
            scope=data['scope'],
            token=token,
            account=None,
        )

    # TODO: just assuming account scope for now...

    # Lookup the account in sql db
    account = g.sql.query(models.Account).get(data['account'])

    # Ensure the token is associated with a live account
    # TODO: make sure deleted_at is in the past...
    if not account or account.deleted_at:
        # That token's no good anymore.  Get rid of it.
        g.redis.delete(key)
        raise AuthenticationError

    # Return valid auth
    return Authentication(
        is_anonymous=True,
        scope=data['scope'],
        token=token,
        account=account,
    )


def get_token_from_header(header):
    """
    Inspect the given header value and retrieve the token from it.

    Returns the token string.
    Raises AuthenticationError.
    """
    if not header:
        raise AuthenticationError('Bad Header')
    splits = header.split()
    if len(splits) != 2:
        raise AuthenticationError('Bad Header')
    auth_type, token = splits
    if auth_type != 'Bearer':
        raise AuthenticationError('Bad Header')
    return token

from collections import namedtuple
import uuid

from screencloud.common import utils
from screencloud.common.exceptions import AuthenticationError
from screencloud.redis import keys
from screencloud.sql import models


#: Available token scopes
ANONYMOUS = ''
ACCOUNT = 'account'


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

def create_anonymous_token(redis_session):
    """
    Generate an auth token with anonymous scope and persist (redis).

    Returns:
        The generated token string.
    """
    token = uuid.uuid4().hex
    key = keys.authentication_token(token)
    data = {
        'scope': ANONYMOUS,
        'last_accessed': utils.timestamp(),
    }
    redis_session.hmset(key, data)
    return token


def lookup(redis_session, sql, token, update_timestamp=True):
    """
    Lookup the given token string in the auth store (redis).

    Returns:
        An Authentication model object.
    Raises:
        AuthenticationError.
    """

    # Lookup the token in redis
    key = keys.authentication_token(token)
    data = redis_session.hgetall(key)

    if not data:
        raise AuthenticationError

    if update_timestamp:
        redis_session.hset(key, 'last_accessed', utils.timestamp())

    # Return valid anonymous auth
    if data['scope'] == ANONYMOUS:
        return Authentication(
            is_anonymous=True,
            scope=data['scope'],
            token=token,
            account=None,
        )

    # TODO: just assuming account scope for now...

    # Lookup the account in sql db
    account = sql.query(models.Account).get(data['account'])

    # Ensure the token is associated with a live account
    # TODO: make sure deleted_at is in the past...
    if not account or account.deleted_at:
        # That token's no good anymore.  Get rid of it.
        redis_session.delete(key)
        raise AuthenticationError

    # Return valid auth
    return Authentication(
        is_anonymous=True,
        scope=data['scope'],
        token=token,
        account=account,
    )

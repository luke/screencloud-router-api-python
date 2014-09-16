from collections import namedtuple
import uuid

from screencloud.common import utils
from screencloud.redis import keys
from screencloud.sql import models
from . import g

#: Token scopes
ANONYMOUS = 'anonymous'
ACCOUNT = 'account'

#: Authentication model to pass around
Auth = namedtuple(
    'Authentication', 
    [
        'is_anonymous',
        'scope',
        'token',
        'account',
    ]
)

def create_anonymous_token():
    token = uuid.uuid4().hex
    key = keys.authentication_token(token)
    data = {
        'scope': ANONYMOUS,
        'last_accessed': utils.timestamp(),
    }
    g.redis.hmset(key, data)
    return token


def lookup(auth_header, update_timestamp=True):
    # Verify the header
    if not auth_header:
        return None
    splits = auth_header.split()
    if len(splits) != 2:
        return None
    auth_type, token = splits
    if auth_type != 'Bearer':
        return None

    # Lookup the token in redis
    key = keys.authentication_token(token)
    data = g.redis.hgetall(key)

    if not data:
        return None

    if update_timestamp:
        g.redis.hset(key, 'last_accessed', utils.timestamp())

    # Return valid anonymous auth
    if data['scope'] == ANONYMOUS:
        return Auth(
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
        return None

    # Return valid auth
    return Auth(
        is_anonymous=True,
        scope=data['scope'],
        token=token,
        account=account,
    )

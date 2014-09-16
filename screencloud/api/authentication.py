import uuid

from screencloud.common import utils
from screencloud.redis import keys

ANONYMOUS = 'anonymous'

def create_anonymous_token(redis):
    token = uuid.uuid4().hex
    key = keys.authentication_token(token)
    data = {
        'account_id': ANONYMOUS,
        'last_accessed': utils.timestamp(),
    }
    redis.hmset(key, data)
    return token


def lookup(redis, auth_header):
    if not auth_header:
        return None

    splits = auth_header.split()
    if len(splits) != 2:
        return None

    auth_type, token = splits
    if auth_type != 'Bearer':
        return None

    key = keys.authentication_token(token)
    account_id = redis.hget(key, 'account_id')

    if not account_id:
        return None

    return account_id

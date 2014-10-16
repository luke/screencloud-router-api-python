from screencloud.common import utils, scopes
from screencloud.common.exceptions import AuthenticationError
from screencloud.redis import models as rmodels
from screencloud.sql import models as smodels


def create_anonymous_auth(redis_session):
    """
    Generate an auth token with anonymous scope and persist.

    Returns:
        An Authentication model object.
    """
    auth = rmodels.Auth()
    auth._rpersist(redis_session)
    return auth


def lookup(redis_session, sql_session, token, update_timestamp=True):
    """
    Lookup the given token string in the auth store (redis).

    Returns:
        An Authentication model object.
    Raises:
        AuthenticationError.
    """

    # Lookup the token in redis
    auth = rmodels.Auth._rlookup(token)

    if not auth:
        raise AuthenticationError

    if update_timestamp:
        ts = utils.timestamp()
        redis_session.hset(auth._rkey, 'last_accessed', ts)
        auth.last_accessed = ts

    # Scope dependant behaviour
    # -------------------------

    # Anonymous
    if not auth.scopes:
        return auth

    # All non-anonymous scopes are expected to have an account
    account = sql_session.query(models.Account).get(auth.data['account_id'])

    # Ensure the token is associated with a live account
    # TODO: make sure deleted_at is in the past...
    if not account or account.deleted_at:
        # That token's no good anymore.  Get rid of it.
        redis_session.delete(auth._rkey)
        raise AuthenticationError

    # Return valid auth
    return auth

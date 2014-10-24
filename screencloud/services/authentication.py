from datetime import datetime

from screencloud.common import utils, scopes, exceptions
from screencloud.redis import models as rmodels
from screencloud.sql import models as smodels

def create_anonymous_auth(connections, persist=True):
    """
    Generate an auth token with anonymous scope.

    Returns:
        An Authentication model object.
    """
    auth = rmodels.Auth()
    if persist:
        auth._rpersist(connections.redis)
    return auth


def create_network_remote_auth(connections, network_id, persist=True):
    """
    Generate auth with scope to do the things a remote app (e.g. the
    ScreenBox iOS app) controlling a (top-level) network would probably want
    to do.

    E.g. Sign-up new users and generate relevant auth tokens for them.

    Returns:
        An Authentication model object.
    """
    auth = rmodels.Auth()
    auth.context = {
        'network': network_id,
    }
    auth.scopes = [
        scopes.NETWORK__READ,
        scopes.USERS__LOGIN,
        scopes.USERS__CREATE
    ]
    if persist:
        auth._rpersist(connections.redis)
    return auth


def create_network_remote_user_auth(connections, network_id, user_id, persist=True):
    """
    Generate auth with scope to do the things a remote app (e.g. the
    ScreenBox iOS app) controlling a (top-level) network would probably want
    to do on behalf of a user.

    E.g. Create accounts (through sub-networks) in that network and generate
    app-instances.

    Returns:
        An Authentication model object.
    """
    auth = rmodels.Auth()
    auth.context = {
        'network': network_id,
        'user': user_id
    }
    auth.scopes = [
        scopes.NETWORK__READ,
        scopes.USER__UPDATE,
        scopes.NETWORK__USER__FULL
    ]
    if persist:
        auth._rpersist(connections.redis)
    return auth


def lookup(connections, token, update_timestamp=True, remove_if_invalid=True):
    """
    Lookup the given token string in the auth store (redis).

    Returns:
        An Authentication model object.
    Raises:
        AuthenticationError.
    """

    # Lookup the token in redis
    auth = rmodels.Auth._rlookup(connections.redis, token)

    if not auth:
        raise exceptions.AuthenticationError

    if update_timestamp:
        ts = utils.timestamp()
        connections.redis.hset(auth._rkey, 'last_accessed', ts)
        auth.last_accessed = ts


    # If the token has a context, ensure the related resources exist.
    for resource_type, resource_id in auth.context.items():
        model = _resource_type_model_map[resource_type]
        resource = connections.sql.query(model).get(resource_id)

        # Ensure the resource is alive.
        if not resource or (
                resource.deleted_at
                and resource.deleted_at < datetime.utcnow()
        ):
            # That token's no good anymore.
            if remove_if_invalid:
                connections.redis.delete(auth._rkey)
            raise exceptions.AuthenticationError

    # Return valid auth
    return auth


#: Helper to lookup resources specified in an auth's context.
_resource_type_model_map = {
    'user': smodels.User,
    'network': smodels.Network,
    'account': smodels.Account,
}

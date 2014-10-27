from datetime import datetime

from screencloud.common import utils, scopes, exceptions
from screencloud.redis import models as rmodels
from screencloud.sql import models as smodels

from . import identities as identity_service

def create_with_identity(connections, user_data, identity_data):
    """
    Create a new user and associated identity using the provided data dicts.

    Returns:
        The new user as a `screencloud.sql.models.User`
    Raises:
        UnprocessableError
    """

    identity = identity_service.create(
        connections,
        identity_data['type'],
        identity_data['identifier'],
        identity_data['data'],
        persist=False
    )

    user = smodels.User()
    user.name = user_data['name']
    user.email = user_data['email']

    identity.user = user
    connections.sql.add(user)
    connections.sql.commit()

    return user


def update(connections, user_id, user_data):
    """
    Update a user using the provided data.

    Returns:
        The updated user as a `screencloud.sql.models.User`
    Raises:
        ResourceMissingError
    """

    user = connections.sql.query(smodels.User).get(user_id)
    if not user:
        raise exceptions.ResourceMissingError({'user' : user_id})
    for k, v in user_data.items():
        setattr(user, k, v)
    connections.sql.commit()

    return user


def lookup_by_valid_identity(connections, identity_data):
    """
    Lookup a user from the provided identity_data.  Also validates the identity.

    Returns:
        The user as a `screencloud.sql.models.User`
    Raises:
        UnprocessableError
    """

    identity = identity_service.lookup_and_verify(
        connections,
        identity_data['type'],
        identity_data['identifier'],
        identity_data['data']
    )

    user = identity.user

    return user

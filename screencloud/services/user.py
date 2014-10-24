from datetime import datetime

from screencloud.common import utils, scopes, exceptions
from screencloud.redis import models as rmodels
from screencloud.sql import models as smodels

from . import identity as identity_service

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

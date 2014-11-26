from datetime import datetime

from screencloud.common import utils, scopes, exceptions
from screencloud.redis import models as rmodels
from screencloud.sql import models as smodels

from . import identities as identity_service

def create_under_network_with_identity(
    connections, network_id, user_data, identity_data
):
    """
    Create a new user and associated identity using the provided data dicts.

    The identity will be namespaced to the given (top-level) network.  We also
    create a default account and network for this user (as a sub-network of the
    given top-level network).

    Expects identity_data like:
        {
            'identifier': 'blah',
            'secret': 'blah'
        }

    Returns:
        The new user as a `screencloud.sql.models.User`
    Raises:
        UnprocessableError
    """

    identity = identity_service.create(
        connections,
        identity_service.BASIC_NAMESPACED_TYPE,
        identity_data['identifier'],
        {
            'secret': identity_data['secret'],
            'namespace': network_id
        },
        persist=False
    )

    user = smodels.User()
    user.name = user_data['name']
    user.email = user_data['email']

    account = smodels.Account()
    user.accounts.append(account)

    network = smodels.Network()
    network.parent_id = network_id
    account.networks.append(network)

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


def lookup(connections, user_id):
    """
    Try to find the user in the system.

    Returns:
        None or `screencloud.sql.models.User`
    """
    return connections.sql.query(smodels.User).get(user_id)


def lookup_by_identity(connections, identity_data):
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


def lookup_by_network_identity(connections, network_id, identity_data):
    """
    Lookup a user from the provided identity_data, using the namespaced identity
    type tied to a given top-level network.  Also validates the identity.

    Expects identity_data like:
        { 
            'identifier': 'blah',
            'secret': 'blah'
        }

    Returns:
        The user as a `screencloud.sql.models.User`
    Raises:
        UnprocessableError
    """
    # We just munge the provided data into the format needed for
    # lookup_by_identity above.
    return lookup_by_identity(
        connections,
        {
            'type': identity_service.BASIC_NAMESPACED_TYPE,
            'identifier': identity_data['identifier'],
            'data': {
                'secret': identity_data['secret'],
                'namespace': network_id
            }
        }
    )

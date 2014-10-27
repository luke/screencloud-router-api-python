from datetime import datetime

from screencloud.common import utils, scopes, exceptions
from screencloud.redis import models as rmodels
from screencloud.sql import models as smodels

def lookup(connections, account_id):
    """
    Try to find the account in the system.

    Returns:
        None or `screencloud.sql.models.Account`
    """
    return connections.sql.query(smodels.Account).get(account_id)


def lookup_all_for_network_user(connections, network_id, user_id):
    """
    Retrieve the list of accounts that are related to the given network and
    user.

    Returns:
        [`screencloud.sql.models.Account`]
    """
    # Limit accounts to only those related to the given network and user
    return connections.sql.query(smodels.Account)\
        .filter(smodels.Account.users.any(id=user_id))\
        .filter(smodels.Account.networks.any(smodels.Network.parent_id==network_id))\
        .all()


def create_for_network_user(connections, network_id, user_id, account_data):
    """
    Create an account using the provided data.  Also creates a new subnetwork
    under the given network and associated to the account.

    Returns:
        The created account as a `screencloud.sql.models.Account`
    """

    network = connections.sql.query(smodels.Network).get(network_id)
    user = connections.sql.query(smodels.User).get(user_id)

    account = smodels.Account()
    subnetwork = smodels.Network()

    account.users.append(user)
    account.networks.append(subnetwork)
    subnetwork.parent = network

    for k, v in account_data.items():
        setattr(account, k, v)

    connections.sql.add(account)
    connections.sql.commit()

    return account


def update(connections, account_id, account_data):
    """
    Update an account using the provided data.

    Returns:
        The updated account as a `screencloud.sql.models.Account`
    Raises:
        ResourceMissingError
    """

    account = connections.sql.query(smodels.Account).get(account_id)
    if not account:
        raise exceptions.ResourceMissingError({'account' : account_id})
    for k, v in account_data.items():
        setattr(account, k, v)
    connections.sql.commit()

    return account

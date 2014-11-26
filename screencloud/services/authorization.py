from screencloud.redis import models as rmodels
from screencloud.sql import models as smodels
from screencloud.common import scopes, utils, exceptions

def assert_can_create_users(connections, auth):
    if scopes.USERS__CREATE in auth.scopes:
        return
    raise exceptions.AuthorizationError


def assert_can_login_users(connections, auth):
    if scopes.USERS__LOGIN in auth.scopes:
        return
    raise exceptions.AuthorizationError


def assert_can_get_user(connections, auth, user_id):
    if scopes.NETWORK__USER__FULL in auth.scopes and auth.context['user'] == user_id:
        return
    raise exceptions.AuthorizationError


def assert_can_update_user(connections, auth, user_id):
    if scopes.USER__UPDATE in auth.scopes and auth.context['user'] == user_id:
        return
    raise exceptions.AuthorizationError


def assert_can_get_accounts(connections, auth):
    if scopes.NETWORK__USER__FULL in auth.scopes:
        return
    raise exceptions.AuthorizationError


def assert_can_create_accounts(connections, auth):
    if scopes.NETWORK__USER__FULL in auth.scopes:
        return
    raise exceptions.AuthorizationError


def assert_can_update_account(connections, auth, account_id):
    if scopes.NETWORK__USER__FULL not in auth.scopes:
        raise exceptions.AuthorizationError

    network = connections.sql.query(smodels.Network).get(
        auth.context['network']
    )
    user = connections.sql.query(smodels.User).get(auth.context['user'])
    account = connections.sql.query(smodels.Account).get(account_id)

    if not account:
        raise exceptions.ResourceMissingError({'account' : account_id})

    if user in account.users and network in account.networks:
        return

    raise exceptions.AuthorizationError


def assert_can_get_account(connections, auth, account_id):
    if scopes.NETWORK__USER__FULL not in auth.scopes:
        raise exceptions.AuthorizationError

    network = connections.sql.query(smodels.Network).get(
        auth.context['network']
    )
    user = connections.sql.query(smodels.User).get(auth.context['user'])
    account = connections.sql.query(smodels.Account).get(account_id)

    if not account:
        raise exceptions.ResourceMissingError({'account' : account_id})

    if user in account.users and network in account.networks:
        return

    raise exceptions.AuthorizationError


def assert_can_create_subhub_jwt_for_network(connections, auth, network_id):
    if scopes.NETWORK__USER__FULL not in auth.scopes:
        raise exceptions.AuthorizationError

    # Network must be a sub-network of the authed network, and must belong to
    # the authed user.
    network = connections.sql.query(smodels.Network).get(network_id)

    if not network:
        raise exceptions.ResourceMissingError({'network' : network_id})

    if network.parent_id != auth.context['network']:
        raise exceptions.AuthorizationError

    linking_account = connections.sql.query(
        smodels.Account
    ).filter(
        smodels.Account.users.any(id=auth.context['user'])
    ).filter(
        smodels.Account.networks.any(id=network_id)
    ).first()

    if not linking_account:
        raise exceptions.AuthorizationError

    return

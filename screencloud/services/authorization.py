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


def assert_can_get_apps(connections, auth):
    if scopes.NETWORK__READ in auth.scopes:
        return
    raise exceptions.AuthorizationError


def assert_can_get_app(connections, auth, app_id):
    if scopes.NETWORK__READ not in auth.scopes:
        raise exceptions.AuthorizationError

    network = connections.sql.query(smodels.Network).get(
        auth.context['network']
    )
    app = connections.sql.query(smodels.App).get(app_id)

    if not app:
        raise exceptions.ResourceMissingError({'app' : app_id})

    if app in network.apps:
        return

    raise exceptions.AuthorizationError

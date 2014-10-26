from screencloud.common import scopes, utils, exceptions

def assert_can_create_users(connections, auth):
    if scopes.USERS__CREATE in auth.scopes:
        return
    raise exceptions.AuthorizationError


def assert_can_login_users(connections, auth):
    if scopes.USERS__LOGIN in auth.scopes:
        return
    raise exceptions.AuthorizationError


def assert_can_update_user(connections, auth, user_id):
    if scopes.USER__UPDATE in auth.scopes and auth.context['user'] == user_id:
        return
    raise exceptions.AuthorizationError

from screencloud.common import scopes, utils, exceptions

def assert_can_create_user(connections, auth):
    if scopes.USERS__CREATE in auth.scopes:
        return
    raise exceptions.AuthorizationError


def assert_can_login_user(connections, auth):
    if scopes.USERS__LOGIN in auth.scopes:
        return
    raise exceptions.AuthorizationError

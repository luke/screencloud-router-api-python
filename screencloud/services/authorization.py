from screencloud.common import scopes
from screencloud.common.exceptions import AuthorizationError

from . import Service

class Authorization(Service):
    def assert_can_create_user(auth):
        raise AuthorizationError

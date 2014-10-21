from datetime import datetime

from screencloud.common import utils, scopes
from screencloud.common.exceptions import AuthenticationError
from screencloud.redis import models as rmodels
from screencloud.sql import models as smodels

from . import Service

class User(Service):
    def create_with_identity(self, user, identity):
        """
        Create a new user and associated identity using the provided data dicts.

        Checks to ensure identity data is unique in the system.

        Returns:
            The new user as a `screencloud.sql.models.User`

        Raises:
            InputError
        """
        return 'hi'

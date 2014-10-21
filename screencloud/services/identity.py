from datetime import datetime

from screencloud.common import utils, scopes
from screencloud.common.exceptions import AuthenticationError
from screencloud.redis import models as rmodels
from screencloud.sql import models as smodels

from . import Service

class Identity(Service):
    def lookup_user(self, identity_type, identifier, data):
        return 'hi'

    def lookup_identity(self, identity_type, identifier, data):
        return 'hi'

from datetime import datetime

from screencloud.common import utils, scopes, exceptions
from screencloud.redis import models as rmodels
from screencloud.sql import models as smodels

def lookup(connections, identity_type, identifier):
    """
    Try to find the identity in the system.

    Returns:
        None or `screencloud.sql.models.Identity`
    """
    return connections.sql.query(smodels.UserIdentity)\
        .filter_by(type=identity_type, identifier=identifier)\
        .first()

def create(connections, identity_type, identifier, data, persist=True):
    """
    Try to find the identity in the system.

    Returns:
        None or `screencloud.sql.models.Identity`
    Raises:
        InputError
    """
    return 'hi'

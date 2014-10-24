from datetime import datetime

from screencloud.common import utils, scopes, exceptions
from screencloud.redis import models as rmodels
from screencloud.sql import models as smodels

BASIC_TYPE = 'basic' # Simple hashed password type.
GOOGLE_TYPE = 'google' # Google OAuth type.

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
    Create an identity from the provided data.  Requirements for the structure
    of `data` depend on the identity type.

    WIll fail if the identifier/identity_type combination already exists.

    Returns:
        None or `screencloud.sql.models.Identity`
    Raises:
        UnprocessableError
    """
    if identity_type != BASIC_TYPE:
        raise NotImplementedError

    return 'hi'

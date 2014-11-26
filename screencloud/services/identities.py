from datetime import datetime

from screencloud.common import utils, scopes, exceptions
from screencloud.redis import models as rmodels
from screencloud.sql import models as smodels

# TODO: make schematics models for the various types so they can be used in
# other parts of the system as safe-ways to input structured data to this
# service.

# Simple hashed password type.
BASIC_TYPE = 'basic'

# Simple hashed password type where the identifier is namespaced to avoid
# clashes.  This is used by consumer apps to create an identity namespaced to
# their top-level network.
BASIC_NAMESPACED_TYPE = 'basic-namespaced'

# Google OAuth type.
GOOGLE_TYPE = 'google'


def lookup(connections, identity_type, identifier):
    """
    Try to find the identity in the system.

    Returns:
        None or `screencloud.sql.models.Identity`
    """
    primary_key_tuple = smodels.UserIdentity._construct_pk_tuple(
        type=identity_type,
        identifier=identifier
    )
    return connections.sql.query(smodels.UserIdentity).get(primary_key_tuple)


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
    # TODO: abstract this stuff out to different identity classes/models

    if identity_type not in [BASIC_TYPE, BASIC_NAMESPACED_TYPE]:
        raise NotImplementedError

    if identity_type == BASIC_NAMESPACED_TYPE:
        identifier = _identifier_to_namespaced(identifier, data['namespace'])

    existing = lookup(connections, identity_type, identifier)

    if existing:
        raise exceptions.UnprocessableError('Identity already exists.')

    identity = smodels.UserIdentity()
    identity.type = identity_type
    identity.identifier = identifier
    identity.data = { 'secret': utils.encrypt_secret(data['secret']) }

    if persist:
        connections.sql.add(identity)
        connections.sql.commit()

    return identity


def lookup_and_verify(connections, identity_type, identifier, data):
    """
    Try to find the identity in the system and verify that the provided data
    matches the saved data.  (e.g. check the secret...)

    Returns:
        `screencloud.sql.models.Identity`
    Raises:
        UnprocessableError
    """
    if identity_type not in [BASIC_TYPE, BASIC_NAMESPACED_TYPE]:
        raise NotImplementedError

    if identity_type == BASIC_NAMESPACED_TYPE:
        identifier = _identifier_to_namespaced(identifier, data['namespace'])

    identity = lookup(connections, identity_type, identifier)

    if not identity:
        raise exceptions.UnprocessableError('Could not verify identity.')

    if not utils.verify_secret(data['secret'], identity.data['secret']):
        raise exceptions.UnprocessableError('Could not verify identity.')

    return identity


def _identifier_to_namespaced(identifier, namespace):
    return '%s:%s' % (namespace, identifier)

def _identifier_from_namespaced(namespaced_identifier, namespace):
    return split(namespaced_identifier+':', namespace)[1]

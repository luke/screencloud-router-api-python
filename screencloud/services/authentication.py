from datetime import datetime

from screencloud.common import utils, scopes
from screencloud.common.exceptions import AuthenticationError, ServiceUsageError
from screencloud.redis import models as rmodels
from screencloud.sql import models as smodels

from . import Service

class Authentication(Service):
    def create_anonymous_auth(self):
        """
        Generate an auth token with anonymous scope and persist.

        Returns:
            An Authentication model object.
        """
        auth = rmodels.Auth()
        auth._rpersist(redis_session)
        return auth


    def create_network_auth(self, account, network):
        """
        Generate an auth token for the given account with network scope set to the
        given network.

        The given network must be owned by the given account.

        Returns:
            An Authentication model object.
        Raises:
            ServiceUsageError.
        """
        if not network in account.networks:
            raise ServiceUsageError('Trying to create auth for a network unrelated'
                                    ' to the given account.')

        auth = rmodels.Auth()
        auth.scopes = [scopes.NETWORK]
        auth.data = {
            'account': account.id,
            'network': network.id,
        }
        auth._rpersist(self.connections.redis)
        return auth


    def lookup(self, token, update_timestamp=True):
        """
        Lookup the given token string in the auth store (redis).

        Returns:
            An Authentication model object.
        Raises:
            AuthenticationError.
        """

        # Lookup the token in redis
        auth = rmodels.Auth._rlookup(self.connections.redis, token)

        if not auth:
            raise AuthenticationError

        if update_timestamp:
            ts = utils.timestamp()
            self.connections.redis.hset(auth._rkey, 'last_accessed', ts)
            auth.last_accessed = ts

        # Scope dependant behaviour
        # -------------------------

        # Anonymous
        if not auth.scopes:
            return auth

        # # All non-anonymous scopes are expected to have an account
        # account = self.connections.sql.query(models.Account)\
        #     .get(auth.data['account_id'])

        # # Ensure the token is associated with a live account
        # if not account or (
        #     account.deleted_at and account.deleted_at < datetime.utcnow()
        # ):
        #     # That token's no good anymore.  Get rid of it.
        #     self.connections.redis.delete(auth._rkey)
        #     raise AuthenticationError

        # Do we want to do more checking here?  E.g. making sure other objects
        # related to the scopes exist in the db?  Dunno... feels like it doesn't
        # belong here.

        # Return valid auth
        return auth

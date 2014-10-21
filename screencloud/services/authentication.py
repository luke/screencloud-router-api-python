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
        auth._rpersist(self.connections.redis)
        return auth


    def create_network_auth(self, network):
        """
        todo

        Returns:
            An Authentication model object.
        """
        auth = rmodels.Auth()
        auth.context = {
            'network': network.id,
        }
        auth.scopes = [scopes.NETWORK__READ, USERS__LOGIN, USERS__CREATE]
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


        # If the token has a context, ensure the related resources exist.
        for resource_type, resource_id in auth.context.items():
            model = _resource_type_model_map['resource_type']
            resource = self.connections.sql.query(model).get(resource_id)
            
            # Ensure the resource is alive.
            if not resource or (
                    resource.deleted_at 
                    and resource.deleted_at < datetime.utcnow()
            ):
                # That token's no good anymore.  Get rid of it.
                self.connections.redis.delete(auth._rkey)
                raise AuthenticationError

        # Return valid auth
        return auth


#: Helper to lookup resources specified in an auth's context.
_resource_type_model_map = {
    'user': smodels.User,
    'network': smodels.Network,
    'account': smodels.Account,
}

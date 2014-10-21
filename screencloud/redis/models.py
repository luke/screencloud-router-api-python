import schematics.models
from schematics.types import StringType, FloatType
from schematics.types.compound import ListType, DictType
from schematics.transforms import whitelist

from screencloud.common import utils
from . import keys

class Base(schematics.models.Model):
    pass

class Auth(Base):
    """
    E.g.

        token = 'GdUxyv4y8AXMU6YvtTyKqNkNy-PEKCLtL8GtchxSLzw='
        context = {
          'user': '25afde59991f4ba5badb28c22e12a925',
          'network': '883e76ab687347448d5fae4650c8cb72'
        }
        scopes = ['user:update', 'network:read', 'network.user:full']
        last_accessed = 1413848222.908317


        token = 'hOJBdUkrdNh8AUbe--bCsnwEB5kU5YP9Eq2wzRBn8Lk='
        context = {
          'network': '938990542ab14ec794c19bdebbdb1506'
        }
        scopes = ['users:login', 'users:create', 'network:read']
        last_accessed = 1413847789.677509

    """

    token = StringType(default=utils.url_safe_token)
    context = DictType(StringType(), default=dict)
    scopes = ListType(StringType(), default=list)
    last_accessed = FloatType(default=utils.timestamp)

    class Options:
        roles = {
            'redis': whitelist('context', 'scopes', 'last_accessed')
        }

    @property
    def _rkey(self):
        return keys.authentication_token(self.token)

    def _rpersist(self, redis_session):
        return redis_session.hmset(self._rkey, self.to_primitive(role='redis'))

    @classmethod
    def _rlookup(cls, redis_session, token):
        k = keys.authentication_token(token)
        d = redis_session.hgetall(k)
        if not d:
            return d
        d.update({'token': token})
        return cls(d)

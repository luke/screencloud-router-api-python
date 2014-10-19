import schematics.models
from schematics.types import StringType, FloatType
from schematics.types.compound import ListType, DictType
from schematics.transforms import whitelist

from screencloud.common import utils
from . import keys

class Base(schematics.models.Model):
    pass

class Auth(Base):
    token = StringType(default=utils.url_safe_token)
    scopes = DictType(StringType(), default=dict)
    last_accessed = FloatType(default=utils.timestamp)

    class Options:
        roles = {
            'redis': whitelist('scopes', 'last_accessed')
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

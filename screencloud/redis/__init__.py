import re

import redis

from screencloud import config

# Parse connection details (host, port, db)
_match = re.match('redis://(?P<host>.+):(?P<port>\d+)/(?P<db>\d+)',
                  config['REDIS_DB_URI'])
if not _match:
    raise Exception('Bad redis connection string: %s' % config['REDIS_DB_URI'])
conn_details = _match.groupdict()

# Note, redis-py clients are threadsafe (no shared state), so we can use a
# shared connection pool.
pool = redis.ConnectionPool(**conn_details)

def client_factory(shared_pool=False):
    if shared_pool:
        return redis.StrictRedis(connection_pool=pool)
    return redis.StrictRedis(**conn_details)

import redis

from screencloud import config

pool = redis.ConnectionPool(**config['REDIS'])

# Note, redis-py clients are threadsafe (no shared state), so we can use a
# shared connection pool.
def client_factory(shared_pool=False):
    if shared_pool:
        return redis.StrictRedis(connection_pool=pool)
    return redis.StrictRedis(**config['REDIS'])

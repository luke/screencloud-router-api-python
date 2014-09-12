import redis

from screencloud import config

# Note, redis is actually threadsafe anyway, so we don't really need to generate
# new clients per-request.  But oh well.
def client_factory():
    return redis.StrictRedis(**config['REDIS'])

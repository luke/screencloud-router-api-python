class Service(object):
    """
    A base class for service objects.

    Attaches the provided connection data.
    """
    def __init__(self, redis_session, sql_session):
        self.connections = ConnectionHolder()
        self.connections.redis = redis_session
        self.connections.sql = sql_session

# Just a couple of dummy classes to add attributes to
class ServiceHolder(object):
    pass

class ConnectionHolder(object):
    pass

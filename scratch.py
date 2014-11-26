"""
This is just a temporary little helper to load up some useful stuff when using
the python cli.
"""

from screencloud import sql, redis
from screencloud.sql import models as smodels
from screencloud.redis import models as rmodels
from screencloud.services import authentication
from screencloud.common import utils

sql_session = sql.session_factory()
redis_session = redis.client_factory()

connections = utils.Connections(redis_session, sql_session)

def create_screenbox_models():
    network = smodels.Network()
    network.name = 'ScreenBox'

    sql_session.add(network)
    sql_session.commit()

    return network

def create_screenbox_auth():
    network = sql_session.query(smodels.Network)\
        .filter_by(name='ScreenBox')\
        .first()

    return authentication.create_consumerapp_auth(connections, network.id)

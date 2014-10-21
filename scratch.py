"""
This is just a temporary little helper to load up some useful stuff when using
the python cli.
"""

from screencloud import sql, redis
from screencloud.sql import models as smodels
from screencloud.redis import models as rmodels
from screencloud.services.authentication import Authentication

sql_session = sql.session_factory()
redis_session = redis.client_factory()
auth_service = Authentication(redis_session, sql_session)

def create_screenbox_models():
    account = smodels.Account()
    account.name = 'ScreenBox'

    remote = smodels.Remote()
    remote.name = 'ScreenBox'
    account.remotes.append(remote)

    network = smodels.Network()
    network.name = 'ScreenBox'
    account.networks.append(network)

    player = smodels.Player()
    player.url = 'http://player.screencloud.io/index.html'
    network.player = player

    app = smodels.App()
    app.name = 'ScreenBox'
    app.setup_link = 'blah'
    app.edit_link = 'blah'
    network.apps.append(app)

    sql_session.add(account)
    sql_session.commit()

    return account, remote, network, player, app

def create_screenbox_auth():
    network = sql_session.query(smodels.Network)\
        .filter_by(name='ScreenBox')\
        .first()

    return auth_service.create_network_remote_auth(network)

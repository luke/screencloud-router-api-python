from screencloud.sql import models

def create_screenbox(sql_session):
    account = models.Account()
    account = account.name = 'ScreenBox'

    network = models.Network()
    network.name = 'ScreenBox'
    account.networks.append(network)

    player = models.Player()
    player.url = 'http://player.screencloud.io/index.html'
    network.player = player

    app = models.App()
    app.name = 'ScreenBox'
    app.setup_link = 'blah'
    app.edit_link = 'blah'
    network.apps.append(app)

    sql_session.add(account)
    sql_session.commit()

def create_screenbox_auth_token(redis_session, sql_session):
    pass

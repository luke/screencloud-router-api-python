from screencloud.sql import models

def create_screenbox(sql_session):
    account = models.Account()
    network = models.Network()
    account.networks.append(network)

    player = models.Player()
    player.url = 'http://player.screencloud.io/index.html'
    network.player = player

    app = models.App()
    app.name = 'ScreenBox'
    network.apps.append(app)

    sql_session.add(account)
    sql_session.commit()

from cosmic.api import API
from cosmic.http import Server

from screencloud import config
from .resources import accounts, users

def create_server(name):
    api = API(name)
    api.model(accounts.Accounts)
    api.model(users.Users)
    server = Server(api, debug=config['DEBUG'])
    # Attach auth middleware here, using server.wsgi_app
    return server

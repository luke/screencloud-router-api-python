from cosmic.api import API
from .resources import accounts, users

def create(name):
    api = API(name)
    api.model(accounts.Accounts)
    api.model(users.Users)
    return api

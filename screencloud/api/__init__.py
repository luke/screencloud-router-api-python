from cosmic.api import API
from .resources import accounts

def create(name):
    api = API(name)
    api.model(accounts.Accounts)
    return api

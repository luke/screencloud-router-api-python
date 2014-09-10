from cosmic.api import API
from . import models

def create(name):
    api = API(name)
    models.attach_to_api(api)
    return api

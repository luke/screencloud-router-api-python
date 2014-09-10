from cosmic.types import required, String
from cosmic.models import BaseModel
from cosmic.exceptions import NotFound

def attach_to_api(api):
    api.model(accounts)


class tests(BaseModel):
    methods = ['get_by_id', 'create', 'update', 'get_list']
    properties = [
        required(u'name', String)
    ]

    @classmethod
    def get_by_id(cls, id):        
        if not (0 <= id < len(test_store)):
            raise NotFound
        return test_store[id]

    @classmethod
    def create(cls, **patch):
        new_id = len(test_store)
        test_store.append(patch)
        import logging
        logging.warn(test_store)
        return new_id, test_store[new_id]

    @classmethod
    def update(cls, id, **patch):
        test_store[id] = patch
        return test_store[id]

    @classmethod
    def get_list(cls):
        return enumerate(test_store)


test_store = []

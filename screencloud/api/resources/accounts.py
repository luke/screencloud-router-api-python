from __future__ import unicode_literals

from cosmic.types import required, String
from cosmic.models import BaseModel
from cosmic.exceptions import NotFound

class Accounts(BaseModel):
    methods = ['get_by_id', 'create', 'update', 'delete', 'get_list']
    properties = [
        required('name', String)
    ]

    @classmethod
    def get_by_id(cls, uuid):        
        pass

    @classmethod
    def create(cls, **patch):
        pass

    @classmethod
    def update(cls, uuid, **patch):
        pass

    @classmethod
    def delete(cls, uuid):
        pass

    @classmethod
    def get_list(cls):
        pass

from __future__ import unicode_literals

from cosmic.types import required, String, DateTime
from cosmic.models import BaseModel
from cosmic.exceptions import NotFound

from screencloud.sql import models
from ...api import g

model = models.User

class Users(BaseModel):
    methods = ['get_by_id', 'create', 'update', 'get_list']
    properties = [
        required('name', String)
    ]

    @classmethod
    def get_by_id(cls, id):
        obj = g.sql_session.query(model).get(id)
        if not obj:
            raise NotFound
        return obj.__dict__

    @classmethod
    def create(cls, **patch):
        obj = model(**patch)
        g.sql_session.add(obj)
        g.sql_session.commit()
        return (obj.id, obj.__dict__)

    @classmethod
    def update(cls, id, **patch):
        obj = g.sql_session.query(model).get(id)
        if not obj:
            raise NotFound
        obj = model(**patch)
        g.sql_session.add(obj)
        g.sql_session.commit()
        return obj.__dict__

    @classmethod
    def get_list(cls):
        return [
            (obj.id, obj.__dict__) 
            for obj in g.sql_session.query(model).all()
        ]

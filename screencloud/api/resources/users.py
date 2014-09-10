from __future__ import unicode_literals

from cosmic.types import required, String, DateTime
from cosmic.models import BaseModel
from cosmic.exceptions import NotFound

from screencloud.sql import models, session

model = models.User

class Users(BaseModel):
    methods = ['get_by_id', 'create', 'update', 'get_list']
    properties = [
        required('name', String),
        required('email', String),
    ]

    @classmethod
    def get_by_id(cls, id):
        obj = session.query(model).get(id)
        if not obj:
            raise NotFound
        return obj.__dict__

    @classmethod
    def create(cls, **patch):
        obj = model(**patch)
        session.add(obj)
        session.commit()
        return (obj.id, obj.__dict__)

    @classmethod
    def update(cls, id, **patch):
        obj = session.query(model).get(id)
        if not obj:
            raise NotFound
        obj = model(**patch)
        session.add(obj)
        session.commit()
        return obj.__dict__

    @classmethod
    def get_list(cls):
        return [
            (obj.id, obj.__dict__) 
            for obj in session.query(model).all()
        ]

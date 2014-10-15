from flask.ext.restful import Resource

from screencloud.common import exceptions
from screencloud.sql import models
from .. import g, schemas

class List(Resource):
    def get(self):
        pass

    def post(self):
        # Can only create an account with anonymous auth
        if not g.auth.is_anonymous:
            raise exceptions.AuthorizationError

        schema = schemas.Account(g.request.get_json())
        schema.validate()
        model = models.Account(**schema.to_native(role='post'))
        g.sql_session.add(model)
        g.sql_session.commit()

        # Make 

        return schema


class Item(Resource):
    def get(self, id):
        pass

    def patch(self, id):
        pass

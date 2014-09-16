from flask.ext.restful import Resource

from screencloud.sql import models
from .. import g, schemas

class List(Resource):
    def get(self):
        pass

    def post(self):
        obj = schemas.Account(g.request.get_json())
        obj.validate()
        return obj


class Item(Resource):
    def get(self, id):
        pass

    def patch(self, id):
        pass

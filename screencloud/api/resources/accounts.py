from flask.ext.restful import Resource

from screencloud.sql import models
from ...api import g

class List(Resource):
    def get(self):
        pass

    def post(self):
        pass


class Item(Resource):
    def get(self, id):
        pass

    def patch(self, id):
        pass

from flask.ext.restful import Resource

from screencloud.services import authorization, authentication, user
from screencloud.common import exceptions
from .. import g, schemas


class PostInput(schemas.Model):
    identity = schemas.ModelType(schemas.IdentityInput, required=True)
    user = schemas.ModelType(schemas.UserInput, required=True)


class List(Resource):
    def get(self):
        raise NotImplementedError

    def post(self):
        raise NotImplementedError

class Item(Resource):
    def get(self, id):
        raise NotImplementedError

    def patch(self, id):
        raise NotImplementedError

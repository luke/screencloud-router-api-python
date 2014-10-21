from flask.ext.restful import Resource

from screencloud.common import exceptions
from .. import g, schemas, utils


class IdentityInput(schemas.Model):
    identifier = schemas.StringType(required=True)
    type = schemas.StringType(required=True)
    data = schemas.DictType(schemas.StringType(), required=True)

class UserInput(schemas.Model):
    name = schemas.StringType(required=True)
    email = schemas.EmailType(required=True)

class PostInput(schemas.Model):
    identity = schemas.ModelType(IdentityInput, required=True)
    user = schemas.ModelType(UserInput, required=True)



class List(Resource):
    def get(self):
        raise NotImplementedError()

    def post(self):
        g.services.authorization.assert_can_create_user(g.auth)
        input_data = utils.validate_input_structure(g.request, PostInput)
        user = g.services.user.create_with_identity(**input_data.to_primitive())
        return user


class Item(Resource):
    def get(self, id):
        raise NotImplementedError()

    def patch(self, id):
        raise NotImplementedError()

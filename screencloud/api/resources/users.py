from flask.ext.restful import Resource

from screencloud.services import authorization, user
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
        authorization.assert_can_create_user(g.connections, g.auth)
        input_data = utils.validate_input_structure(g.request, PostInput)
        u = user.create_with_identity(
            g.connections,
            user_data=input_data.user.to_primitive(),
            identity_data=input_data.identity.to_primitive()
        )
        return u


class Item(Resource):
    def get(self, id):
        raise NotImplementedError()

    def patch(self, id):
        raise NotImplementedError()

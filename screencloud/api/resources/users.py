from flask.ext.restful import Resource

from screencloud.services import authorization, authentication, user
from screencloud.common import exceptions
from ..actions.tokens import AuthResponse
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


class UserResponse(schemas.Model):
    name = schemas.StringType()
    email = schemas.EmailType()


class List(Resource):
    def get(self):
        raise NotImplementedError

    def post(self):
        authorization.assert_can_create_user(g.connections, g.auth)
        input_data = utils.validate_input_structure(g.request, PostInput)
        u = user.create_with_identity(
            g.connections,
            user_data=input_data.user.to_primitive(),
            identity_data=input_data.identity.to_primitive()
        )
        a = authentication.create_network_remote_user_auth(
            g.connections,
            network_id=g.auth.context['network'],
            user_id=u.id,
        )

        return {
            'user': UserResponse(u._to_dict()),
            'auth': AuthResponse(a.to_primitive())
        }


class Item(Resource):
    def get(self, id):
        raise NotImplementedError

    def patch(self, id):
        raise NotImplementedError

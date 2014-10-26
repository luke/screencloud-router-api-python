from flask.ext.restful import Resource

from screencloud.services import authorization, authentication, user
from screencloud.common import exceptions
from .. import g, schemas


class PostInput(schemas.Model):
    identity = schemas.ModelType(schemas.IdentityInput, required=True)
    user = schemas.ModelType(schemas.UserInput, required=True)

class PatchInput(schemas.Model):
    user = schemas.ModelType(schemas.UserInput, required=True)


class List(Resource):
    def get(self):
        raise NotImplementedError

    def post(self):
        authorization.assert_can_create_users(g.connections, g.auth)
        input_data = schemas.validate_input_structure(g.request, PostInput)
        u = user.create_with_identity(
            g.connections,
            user_data=input_data.user.to_native(),
            identity_data=input_data.identity.to_native()
        )
        a = authentication.create_network_remote_user_auth(
            g.connections,
            network_id=g.auth.context['network'],
            user_id=u.id,
        )

        return {
            'user': schemas.UserResponse(u._to_dict()),
            'auth': schemas.AuthResponse(a.to_primitive())
        }


class Item(Resource):
    def get(self, id):
        if id == 'self':
            id = g.auth.context['user']
        raise NotImplementedError

    def patch(self, id):
        if id == 'self':
            id = g.auth.context['user']
        authorization.assert_can_update_user(g.connections, g.auth, id)
        input_data = schemas.validate_input_structure(
            g.request, PatchInput, partial=True
        )
        u = user.update(
            g.connections,
            user_id=id,
            user_data=input_data.user.to_native(),
        )

        return {
            'user': schemas.UserResponse(u._to_dict()),
        }

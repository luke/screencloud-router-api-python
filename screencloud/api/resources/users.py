from flask.ext.restful import Resource

from screencloud import services
from screencloud.services import authorization
from screencloud.common import exceptions
from .. import g, schemas


class PostInput(schemas.Model):
    identity = schemas.ModelType(schemas.NetworkIdentityInput, required=True)
    user = schemas.ModelType(schemas.UserInput, required=True)

class PatchInput(schemas.Model):
    user = schemas.ModelType(schemas.UserInput, required=True)


class List(Resource):
    def get(self):
        raise NotImplementedError

    def post(self):
        authorization.assert_can_create_users(g.connections, g.auth)
        input_data = schemas.validate_input_structure(g.request, PostInput)

        user, account = services.users.create_under_network_with_identity(
            g.connections,
            network_id=g.auth.context['network'],
            user_data=input_data.user.to_native(),
            identity_data=input_data.identity.to_native()
        )
        auth = services.authentication.create_consumerapp_user_auth(
            g.connections,
            network_id=g.auth.context['network'],
            user_id=user.id,
        )
        return {
            'user': schemas.UserResponse.from_object(user),
            'auth': schemas.AuthResponse.from_object(auth)
        }, 201


class Item(Resource):
    def get(self, id):
        if id == 'self':
            id = g.auth.context['user']
        authorization.assert_can_get_user(g.connections, g.auth, id)
        user = services.users.lookup(g.connections, id)
        return {
            'user': schemas.UserResponse.from_object(user)
        }

    def patch(self, id):
        if id == 'self':
            id = g.auth.context['user']
        authorization.assert_can_update_user(g.connections, g.auth, id)
        input_data = schemas.validate_input_structure(
            g.request, PatchInput, partial=True
        )
        user = services.users.update(
            g.connections,
            user_id=id,
            user_data=input_data.user.to_native(),
        )
        return {
            'user': schemas.UserResponse.from_object(user)
        }

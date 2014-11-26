from flask.ext.restful import Resource

from screencloud import services
from screencloud.services import authorization
from screencloud.common import utils, exceptions
from .. import g, schemas

class LoginInput(schemas.Model):
    identity = schemas.ModelType(schemas.IdentityInput, required=True)


class Login(Resource):
    def post(self):
        authorization.assert_can_login_users(g.connections, g.auth)
        input_data = schemas.validate_input_structure(g.request, LoginInput)
        user = services.users.lookup_by_valid_identity(
            g.connections, 
            input_data.identity.to_native()
        )
        auth = services.authentication.create_consumerapp_user_auth(
            g.connections,
            network_id=g.auth.context['network'],
            user_id=user.id,
        )

        return {
            'user': schemas.UserResponse.from_object(user),
            'auth': schemas.AuthResponse.from_object(auth)
        }

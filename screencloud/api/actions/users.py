from flask.ext.restful import Resource

from screencloud.common import utils, exceptions
from screencloud.services import authentication, authorization, user
from .. import g, schemas

class LoginInput(schemas.Model):
    identity = schemas.ModelType(schemas.IdentityInput, required=True)


class Login(Resource):
    def post(self):
        authorization.assert_can_login_users(g.connections, g.auth)
        input_data = schemas.validate_input_structure(g.request, LoginInput)
        u = user.lookup_by_valid_identity(
            g.connections, 
            input_data.identity.to_native()
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

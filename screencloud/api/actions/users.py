from flask.ext.restful import Resource

from screencloud.common import utils, exceptions
from screencloud.services import authentication, authorization, user
from .. import g, schemas

class LoginInput(schemas.Model):
    identity = schemas.ModelType(schemas.IdentityInput, required=True)


class Login(Resource):
    def post(self):
        authorization.assert_can_login_user(g.connections, g.auth)
        input_data = schemas.validate_input_structure(g.request, LoginInput)

        u = user.lookup_by_valid_identity(g.connections, input_data.to_native())
        a = {}

        return {
            'user': schemas.UserResponse(u._to_dict()),
            'auth': a #schemas.AuthResponse(a.to_privitive())
        }

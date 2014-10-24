from flask.ext.restful import Resource

from screencloud.services import authentication
from .. import g, schemas

class AuthResponse(schemas.HalModel):
    token = schemas.StringType()
    scopes = schemas.ListType(schemas.StringType())


class Anonymous(Resource):
    def post(self):
        auth = authentication.create_anonymous_auth(g.connections)
        return {
            'auth': AuthResponse(auth.to_primitive())
        }

class Verify(Resource):
    def get(self):
        return {
            'auth': AuthResponse(g.auth.to_primitive())
        }

from flask.ext.restful import Resource

from screencloud import services
from .. import g, schemas


class Anonymous(Resource):
    def post(self):
        auth = services.authentication.create_anonymous_auth(g.connections)
        return {
            'auth': schemas.AuthResponse(auth.to_primitive())
        }

class Verify(Resource):
    def get(self):
        return {
            'auth': schemas.AuthResponse(g.auth.to_primitive())
        }

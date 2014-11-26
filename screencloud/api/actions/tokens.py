from flask.ext.restful import Resource

from screencloud import services, config
from .. import g, schemas

class Verify(Resource):
    def get(self):
        return {
            'auth': schemas.AuthResponse.from_object(g.auth)
        }

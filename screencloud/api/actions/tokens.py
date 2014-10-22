from flask.ext.restful import Resource

from screencloud.services import authentication
from .. import g

class Anonymous(Resource):
    def post(self):
        auth = authentication.create_anonymous_auth(g.connections)
        return {
            'token': auth.token
        }

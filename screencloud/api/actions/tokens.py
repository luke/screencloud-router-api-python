from flask.ext.restful import Resource

from .. import g

class Anonymous(Resource):
    def post(self):
        auth = g.services.authentication.create_anonymous_auth()
        return {
            'token': auth.token
        }

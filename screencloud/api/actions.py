from flask.ext.restful import Resource

from screencloud.common import utils
from . import g, authentication

class Tokens(Resource):
    def post(self):
        token = authentication.create_anonymous_token()
        return {
            'token': token
        }

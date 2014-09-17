from flask.ext.restful import Resource

from screencloud.common import utils
from .. import g
from ..auth import authentication

class Anonymous(Resource):
    def post(self):
        token = authentication.create_anonymous_token()
        return {
            'token': token
        }

class Login(Resource):
    def post(self):
        raise NotImplementedError

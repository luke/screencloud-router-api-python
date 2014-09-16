from flask.ext.restful import Resource

from . import g, schemas

class Tokens(Resource):
    def post(self):
        return 'hi'

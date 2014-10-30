from flask.ext.restful import Resource
import firebase_token_generator

from screencloud import services, config
from .. import g, schemas


class Anonymous(Resource):
    def post(self):
        auth = services.authentication.create_anonymous_auth(g.connections)
        return {
            'auth': schemas.AuthResponse.from_object(auth)
        }

class Verify(Resource):
    def get(self):
        return {
            'auth': schemas.AuthResponse.from_object(g.auth)
        }

class PubSub(Resource):
    def get(self):
        jwt = firebase_token_generator.create_token(
            config.get('PUBSUB_SECRET'),
            {
                'uid': 'blah'
            }
        )
        return {
            'uri': config.get('PUBSUB_URI'),
            'token': jwt
        }

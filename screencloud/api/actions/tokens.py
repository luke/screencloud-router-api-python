from flask.ext.restful import Resource

from screencloud import services, config
from .. import g, schemas


# class Anonymous(Resource):
#     def post(self):
#         auth = services.authentication.create_anonymous_auth(g.connections)
#         return {
#             'auth': schemas.AuthResponse.from_object(auth)
#         }

class Verify(Resource):
    def get(self):
        return {
            'auth': schemas.AuthResponse.from_object(g.auth)
        }

class SubHub(Resource):
    def get(self):
        services.authorization.assert_can_access_subhub_for_network_user(
            g.connections, g.auth
        )
        jwt = services.subhub.create_jwt_for_network_user(
            g.connections,
            user_id=g.auth.context['user'],
            network_id=g.auth.context['network']
        )
        return {
            'uri': config.get('SUBHUB_URI'),
            'jwt': jwt
        }

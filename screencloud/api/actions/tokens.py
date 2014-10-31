from flask.ext.restful import Resource

from screencloud import services, config
from .. import g, schemas

class SubHubPostInput(schemas.Model):
    network_id = schemas.StringType(required=True)

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
    def post(self):
        input_data = schemas.validate_input_structure(
            g.request, SubHubPostInput
        )
        services.authorization.assert_can_create_subhub_jwt_for_network(
            g.connections, g.auth, input_data.network_id
        )
        jwt = services.subhub.create_jwt_for_network_user(
            g.connections,
            user_id=g.auth.context['user'],
            network_id=input_data.network_id
        )
        return {
            'uri': config.get('SUBHUB_URI'),
            'jwt': jwt
        }

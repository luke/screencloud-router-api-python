from flask.ext.restful import Resource

from screencloud import services
from screencloud.services import authorization
from screencloud.common import utils, exceptions
from .. import g, schemas


class ExchangeTicketInput(schemas.Model):
    ticket = schemas.StringType(required=True)


class ExchangeTicket(Resource):
    """
    Screens exchange a ticket (see `actions.networks.GenerateScreenTicket`) for
    a uuid and token permitting access to the subhub.
    """
    def post(self):
        input_data = schemas.validate_input_structure(
            g.request, ExchangeTicketInput
        )
        network = services.screens.lookup_network_from_ticket(input_data.ticket)
        import uuid
        screen_id = uuid.uuid4().hex
        return {}




# class SubHubPostInput(schemas.Model):
#     network_id = schemas.StringType(required=True)


# class SubHub(Resource):
#     def post(self):
#         input_data = schemas.validate_input_structure(
#             g.request, SubHubPostInput
#         )
#         services.authorization.assert_can_create_subhub_jwt_for_network(
#             g.connections, g.auth, input_data.network_id
#         )
#         jwt = services.subhub.create_jwt_for_network_user(
#             g.connections,
#             user_id=g.auth.context['user'],
#             network_id=input_data.network_id
#         )
#         return {
#             'uri': config.get('SUBHUB_URI'),
#             'jwt': jwt
#         }

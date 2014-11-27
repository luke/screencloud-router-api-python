from flask.ext.restful import Resource

from screencloud import config, services
from screencloud.services import authorization
from screencloud.common import utils, exceptions
from .. import g, schemas

class GenerateTicketInput(schemas.Model):
    network_id = schemas.StringType(required=True)

class ExchangeTicketInput(schemas.Model):
    ticket = schemas.StringType(required=True)


class GenerateTicket(Resource):
    """
    Tickets are passed to screens by the remote app when connecting to the
    screen and attempting to take it over.
    """
    def post(self):
        input_data = schemas.validate_input_structure(
            g.request, GenerateTicketInput
        )
        network_id = input_data.network_id
        authorization.assert_can_generate_screen_ticket_for_network(
            g.connections, g.auth, network_id
        )
        ticket = services.screens.create_ticket_for_network(
            g.connections, network_id
        )
        return {
            'ticket': ticket
        }


class ExchangeTicket(Resource):
    """
    Screens exchange a ticket (see `GenerateScreenTicket`) for a uuid and token
    permitting access to the subhub.
    """
    def post(self):
        input_data = schemas.validate_input_structure(
            g.request, ExchangeTicketInput
        )
        uuid, jwt = services.screens.exchange_ticket_for_access(
            g.connections, input_data.ticket
        )

        return {
            'uri': config.get('SUBHUB_URI'),
            'uuid': uuid,
            'token': jwt
        }

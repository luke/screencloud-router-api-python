from flask.ext.restful import Resource

from screencloud import services
from screencloud.services import authorization
from screencloud.common import utils, exceptions
from .. import g, schemas


class GenerateTicket(Resource):
    """
    Tickets are passed to screens by the remote app when connecting to the
    screen and attempting to take it over.
    """
    def post(self, network_id):
        authorization.assert_can_generate_screen_ticket_for_network(
            g.connections, g.auth, network_id
        )
        ticket = services.screens.create_ticket(g.connections, network_id)
        return {
            'ticket': ticket
        }

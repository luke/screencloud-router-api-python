from screencloud import config
from screencloud.common import utils, scopes, exceptions
from screencloud.redis import keys, models as rmodels
from screencloud.sql import models as smodels

def create_ticket_for_network(connections, network_id):
    """
    Create a new ticket to be passed to a screen tied to the given network.

    Tickets expire according to SCREEN_TICKET_EXPIRY.

    Returns:
        The generated ticket
    """
    # Generate a random ticket token
    ticket = utils.url_safe_token()

    # Persist the ticket in redis
    connections.redis.set(
        keys.screen_ticket(ticket),
        network_id
        ex=config.get('SCREEN_TICKET_EXPIRY')
    )
    return ticket


def lookup_network_from_ticket(connections, ticket):
    """
    Try to find the screen ticket in redis and the corresponding network in sql.

    Returns:
        The `screencloud.sql.models.Network` related to the provided ticket
    Raises:
        UnprocessableError
    """
    # Lookup the ticket in redis
    network_id = connections.redis.get(keys.screen_ticket(ticket))

    if not network_id:
        raise exceptions.UnprocessableError({'ticket': 'No such ticket.'})

    # Lookup the network in sql
    network = connections.sql.query(smodels.Network).get(network_id)

    if not network:
        raise exceptions.UnprocessableError({'ticket': 'No such ticket.'})

    return network

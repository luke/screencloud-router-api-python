from datetime import datetime

from screencloud.common import utils, scopes, exceptions
from screencloud.redis import models as rmodels
from screencloud.sql import models as smodels

def lookup(connections, app_id):
    """
    Try to find the app in the system.

    Returns:
        None or `screencloud.sql.models.App`
    """
    return connections.sql.query(smodels.App).get(app_id)


def lookup_all_for_network(connections, network_id):
    """
    Retrieve the list of apps within the given network.

    Returns:
        [`screencloud.sql.models.App`]
    """
    return connections.sql.query(smodels.App)\
        .filter_by(network_id=network_id)\
        .all()

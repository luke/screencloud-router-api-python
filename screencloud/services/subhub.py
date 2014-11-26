from firebase_token_generator import create_token

from screencloud import config
from screencloud.common import utils, scopes, exceptions
from screencloud.redis import models as rmodels
from screencloud.sql import models as smodels

def create_jwt_for_network_user(connections, network_id, user_id):
    jwt = create_token(
        config.get('SUBHUB_SECRET'),
        {
            'uid': user_id,
            'user_id': user_id,
            'network_id': network_id
        }
    )
    return jwt

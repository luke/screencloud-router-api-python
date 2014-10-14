import json

from flask import Blueprint

from screencloud import config
from .. import g

bp = Blueprint(__name__, __name__)

@bp.route('/ping', methods=['GET'])
def ping():
    return json.dumps({'echolocation': True})

from flask import Blueprint

bp = Blueprint(__name__, __name__)

@bp.route('/google')
def index():
    return 'Google Login'


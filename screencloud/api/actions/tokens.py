from flask.ext.restful import Resource
from oauth2client.client import OAuth2WebServerFlow

from screencloud.common import utils, exceptions
from screencloud.sql import models
from .. import g
from ..auth import authentication

class Anonymous(Resource):
    def post(self):
        token = authentication.create_anonymous_token()
        return {
            'token': token
        }

class Login(Resource):
    def post(self):
        code = g.request.form.get('code', None)

        if not code:
            raise exceptions.InputError

        flow = OAuth2WebServerFlow(
            client_id=config['OAUTH_CLIENTS']['google']['client_id'],
            client_secret=config['OAUTH_CLIENTS']['google']['client_secret'],
            scope='',
            redirect_uri='postmessage'
        )
        credentials = flow.step2_exchange(code)
        #validate credentials here...
        # credentials.id_token

        id_type = models.UserIdentity.TYPES.GOOGLE
        identifier = credientials.id_token['sub']

        # Look up the user identity
        user_identity = g.sql.query(models.UserIdentity).get([id_type, identifier])

        return credentials.token_response

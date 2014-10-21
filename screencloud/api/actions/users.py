from flask.ext.restful import Resource

from screencloud.common import utils, exceptions
from .. import g, schemas, utils

class LoginInput(schemas.Model):
    identifier = schemas.StringType(required=True)
    type = schemas.StringType(required=True)
    data = schemas.StringType(required=True)


class Login(Resource):
    def post(self):
        input_data = utils.validate_input(g.request, LoginInput)

        # code = g.request.form.get('code', None)

        # if not code:
        #     raise exceptions.InputError

        # from oauth2client.client import OAuth2WebServerFlow
        # flow = OAuth2WebServerFlow(
        #     client_id=config['OAUTH_CLIENTS']['google']['client_id'],
        #     client_secret=config['OAUTH_CLIENTS']['google']['client_secret'],
        #     scope='',
        #     redirect_uri='postmessage'
        # )
        # credentials = flow.step2_exchange(code)
        # #validate credentials here...
        # # credentials.id_token

        # id_type = models.UserIdentity.TYPES.GOOGLE
        # identifier = credientials.id_token['sub']

        # # Look up the user identity
        # user_identity = g.sql_session.query(models.UserIdentity).get([id_type, identifier])

        # return credentials.token_response

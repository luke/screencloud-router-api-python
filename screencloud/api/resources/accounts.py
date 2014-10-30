from flask.ext.restful import Resource

from screencloud import services
from screencloud.services import authorization
from screencloud.common import exceptions
from .. import g, schemas


class PostInput(schemas.Model):
    account = schemas.ModelType(schemas.AccountInput, required=True)


class List(Resource):
    def get(self):
        authorization.assert_can_get_accounts(g.connections, g.auth)
        accounts = services.accounts.lookup_all_for_network_user(
            g.connections,
            network_id=g.auth.context['network'],
            user_id=g.auth.context['user']
        )

        return {
            'accounts': [
                schemas.AccountResponse.from_object(a) for a in accounts
            ]
        }

    def post(self):
        authorization.assert_can_create_accounts(g.connections, g.auth)
        input_data = schemas.validate_input_structure(g.request, PostInput)
        account = services.accounts.create_for_network_user(
            g.connections,
            network_id=g.auth.context['network'],
            user_id=g.auth.context['user'],
            account_data=input_data.account.to_native(),
        )
        return {
            'account': schemas.AccountResponse.from_object(account)
        }, 201


class Item(Resource):
    def get(self, id):
        authorization.assert_can_get_account(g.connections, g.auth, id)
        account = services.accounts.lookup(g.connections, id)
        return {
            'account': schemas.AccountResponse.from_object(account)
        }

    def patch(self, id):
        authorization.assert_can_update_account(g.connections, g.auth, id)
        input_data = schemas.validate_input_structure(g.request, PostInput)
        account = services.accounts.update(
            g.connections,
            account_id=id,
            account_data=input_data.account.to_native(),
        )
        return {
            'account': schemas.AccountResponse.from_object(account)
        }

from flask.ext.restful import Resource

from screencloud import services
from screencloud.services import authorization
from screencloud.common import exceptions
from .. import g, schemas


class List(Resource):
    def get(self):
        authorization.assert_can_get_apps(g.connections, g.auth)
        apps = services.apps.lookup_all_for_network(
            g.connections,
            network_id=g.auth.context['network']
        )
        return {
            'apps': [
                schemas.AppResponse.from_object(a) for a in apps
            ]
        }


class Item(Resource):
    def get(self, id):
        authorization.assert_can_get_app(g.connections, g.auth, id)
        app = services.apps.lookup(g.connections, id)
        return {
            'app': schemas.AppResponse.from_object(app)
        }

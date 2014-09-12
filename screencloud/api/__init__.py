from werkzeug.local import Local, LocalManager
from cosmic.api import API
from cosmic.http import Server

from screencloud import config, sql

# Our global (per request) object.  Not using cosmic's ThreadLocalDict as I
# don't trust it to cleanup after each request when the app is not running as
# unique thread per request.
g = Local()
local_manager = LocalManager([g])

class CustomServer(Server):
    def view(self, endpoint, request, **url_args):
        # Attach some useful stuff
        g.endpoint = endpoint
        g.request = request
        g.sql_session = sql.session_factory()

        try:
            # Authenticate the request

            # Authorize the request

            # Run the API view
            resp = super(CustomServer, self).view(endpoint, request, **url_args)
            return resp
        except:
            g.sql_session.rollback()
            raise
        finally:
            g.sql_session.close()


def create_app(name):
    """Create a WSGI app for this API."""

    from .resources import accounts, users

    api = API(name)
    api.model(accounts.Accounts)
    api.model(users.Users)
    server = CustomServer(api, debug=config['DEBUG'])
    # Werkzeug middleware to ensure a clean 'g' object per request.
    server.wsgi_app = local_manager.make_middleware(server.wsgi_app)
    return server.wsgi_app

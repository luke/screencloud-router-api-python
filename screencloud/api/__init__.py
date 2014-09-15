from werkzeug.local import Local, LocalManager
from werkzeug.wsgi import DispatcherMiddleware

# Our global (per request) object.  Framework agnostic to make it easier to
# switch things.
#
# We make it available early so that we can import it in submodules of this
# module (and still import the submodules in here).
g = Local()

from flask import Flask
from flask.ext.restful import Api

from screencloud import config, sql, redis
from .resources import accounts
# from . import authentication, authorization, representations


class CustomApi(Api):
    def add_resource(self, resource, *urls, **kwargs):
        """Add a resource endpoint to the api.

        We patch the flask-restful version to use {module}.{class_name} for the
        endpoint (it just does class_name by default).  Otherwise we can't name
        classes the same inside the resource modules, e.g. can't have both
        accounts.List and users.List without passing endpoint='somethingunique'
        everytime we call api.add_resource.  This is also helpful when using
        fields.Url().
        """
        if 'endpoint' not in kwargs:
            mod_name, cls_name = resource.__module__, resource.__name__
            kwargs['endpoint'] = '%s.%s' % (mod_name.split('.')[-1],  cls_name)
        return super(CustomApi, self).add_resource(resource, *urls, **kwargs)




def create_wsgi_app(name):
    """Create a WSGI app for this API."""

    app = Flask(name)
    app.config.update(config)
    api = CustomApi(app, prefix='', catch_all_404s=True)

    @app.before_request
    def br_authenticate():
        pass

    @app.before_request
    def br_authorize():
        pass


    # Set up handlers to represent our schemas
    # @api.representation('application/json')
    # representations.json

    # @api.representation('application/hal+json')
    # representations.hal_json


    # Attach the api routes
    api.add_resource(accounts.List, '/accounts')
    api.add_resource(accounts.Item, '/accounts/<string:id>')


    # Werkzeug middleware to ensure a clean 'g' object per request.
    local_manager = LocalManager([g])
    app.wsgi_app = local_manager.make_middleware(app.wsgi_app)

    return app.wsgi_app

from flask import Flask, request
from flask.ext.restful import Api as BaseApi, abort

from screencloud import config, sql, redis
from . import g, local_manager
from . import representations
from . import authentication, authorization
from . import actions
from .resources import accounts


class Api(BaseApi):
    def __init__(self, *args, **kwargs):
        super(Api, self).__init__(*args, **kwargs)
        self.representations = {
            'application/json': representations.to_json,
            'application/hal+json': representations.to_hal_json
        }
        self.public_endpoints = set()

    def add_resource(self, resource, *urls, **kwargs):
        """Add a resource endpoint to the api.

        We patch the flask-restful version to use {module}.{class_name} for the
        endpoint (it just does class_name by default).  Otherwise we can't name
        classes the same inside the resource modules, e.g. can't have both
        accounts.List and users.List without passing endpoint='somethingunique'
        everytime we call api.add_resource.  This is also helpful when using
        fields.Url().

        We also add an additional kwarg 'public::Bool' to specify that the
        resource doesn't need auth checked.
        """
        if 'endpoint' not in kwargs:
            mod_name, cls_name = resource.__module__, resource.__name__
            kwargs['endpoint'] = '%s.%s' % (mod_name.split('.')[-1],  cls_name)

        if 'public' in kwargs:
            kwargs.pop('public')
            self.public_endpoints.add(kwargs['endpoint'])

        return super(Api, self).add_resource(resource, *urls, **kwargs)




def create_wsgi_app(name):
    """Create a WSGI app for this API."""

    app = Flask(name)
    app.config.update(config)
    api = Api(
        app,
        prefix='',
        default_mediatype='application/json',
        catch_all_404s=True
    )


    @app.before_request
    def attach_globals():
        """Attach useful, request-long, objects to the global g."""
        g.request = request
        g.sql = sql.session_factory()
        g.redis = redis.client_factory(shared_pool=True)


    @app.teardown_request
    def cleanup(exc):
        """Ensure any used resources are cleaned up after the request."""
        if exc:
            g.sql.rollback()
        g.sql.close()


    @app.before_request
    def br_authenticate():
        """Attach an Authentication object to the global at `g.auth`.

        Don't check routes outside the api, or routes declared public.
        (Set `g.auth = None` in this case, and carry on)
        """
        if request.endpoint not in (api.endpoints - api.public_endpoints):
            g.auth = None
            return

        g.auth = authentication.lookup(
            g.request.headers.get('Authorization', None)
        )
        if not g.auth:
            abort(401)


    @app.before_request
    def br_authorize():
        #TODO: ... acl stuff ...
        pass


    # Attach the api REST resource routes
    api.add_resource(accounts.List, '/accounts')
    api.add_resource(accounts.Item, '/accounts/<string:id>')

    # Attach the api action routes (not necessarily RESTy)
    api.add_resource(actions.Tokens, '/tokens', public=True)

    # Werkzeug middleware to ensure a clean 'g' object per request.
    app.wsgi_app = local_manager.make_middleware(app.wsgi_app)

    return app.wsgi_app

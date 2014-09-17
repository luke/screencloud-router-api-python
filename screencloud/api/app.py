from flask import Flask, request
from flask.ext.restful import Api as BaseApi
import schematics.exceptions

from screencloud import config, sql, redis
from screencloud.common import exceptions
from . import g, local_manager
from . import representations
from .auth import scopes, authentication, authorization
from . import actions, resources, views


class Api(BaseApi):
    """
    Customized subclass of the flask-restful Api.
    """

    def __init__(self, *args, **kwargs):
        super(Api, self).__init__(*args, **kwargs)
        self.representations = {
            'application/json': representations.to_json,
            'application/hal+json': representations.to_hal_json
        }
        self.public_endpoints = set()


    def add_resource(self, resource, *urls, **kwargs):
        """
        Add a resource endpoint to the api.

        We patch the flask-restful version to use {module}.{class_name} for the
        endpoint (it just does class_name by default).  Otherwise we can't name
        classes the same inside the resource modules, e.g. can't have both
        accounts.List and users.List without passing endpoint='somethingunique'
        everytime we call api.add_resource.  This is also helpful when using
        fields.Url().

        We also add additional kwarg options:

          public (bool): Specify that the resource doesn't need auth checked.

        """
        if 'endpoint' not in kwargs:
            mod_name, cls_name = resource.__module__, resource.__name__
            kwargs['endpoint'] = '%s.%s' % (mod_name.split('.')[-1],  cls_name)

        if 'public' in kwargs:
            kwargs.pop('public')
            self.public_endpoints.add(kwargs['endpoint'])

        return super(Api, self).add_resource(resource, *urls, **kwargs)


    def handle_error(self, err):
        """
        Handle standard expections raised in the app and respond appropriately.
        """
        def make_response(data, code):
            resp = {'status': code}
            resp.update(data)
            return representations.to_json(resp, code)

        if isinstance(err, exceptions.AuthenticationError):
            return make_response({'message': 'Unauthorized',}, 401)

        if isinstance(err, exceptions.AuthorizationError):
            return make_response({'message': 'Forbidden',}, 403)

        if isinstance(err, schematics.exceptions.ValidationError):
            return make_response(
                {
                    'message': 'Bad Request',
                    'errors': err.message
                }, 400
            )

        return super(Api, self).handle_error(err)





def create_wsgi_app(name):
    """
    Create a WSGI app for this API.
    """

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
        """
        Attach useful, request-long, objects to the global g.
        """
        g.request = request
        g.sql = sql.session_factory()
        g.redis = redis.client_factory(shared_pool=True)


    @app.teardown_request
    def cleanup(exc):
        """
        Ensure any used resources are cleaned up after the request.
        """
        if g.sql:
            if exc:
                g.sql.rollback()
            g.sql.close()


    @app.before_request
    def br_authenticate():
        """
        Attach an Authentication object to the global at `g.auth`.

        Doesn't check routes outside the api, or routes declared public.
        (Sets `g.auth = None` in this case)

        Raises:
            AuthenticationError.
        """
        if request.endpoint not in (api.endpoints - api.public_endpoints):
            g.auth = None
            return

        header = g.request.headers.get('Authorization', None)
        token = authentication.get_token_from_header(header)
        g.auth = authentication.lookup(token)


    @app.before_request
    def br_authorize():
        #TODO: ... acl stuff ...
        pass


    # Attach the api REST resource routes
    api.add_resource(resources.accounts.List, '/accounts')
    api.add_resource(resources.accounts.Item, '/accounts/<string:id>')

    # Attach the api action routes (not necessarily RESTy)
    api.add_resource(actions.tokens.Anonymous, '/tokens/anonymous', public=True)
    api.add_resource(actions.tokens.Login, '/tokens/login', public=True)

    # Attach non-api routes
    app.register_blueprint(views.testing.bp, url_prefix='/testing')

    # Werkzeug middleware to ensure a clean 'g' object per request.
    app.wsgi_app = local_manager.make_middleware(app.wsgi_app)

    return app.wsgi_app

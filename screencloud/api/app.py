from flask import Flask, request, jsonify
from flask.ext.restful import Api as BaseApi
import schematics.exceptions

from screencloud import config, sql, redis
from screencloud.services import authentication, authorization
from screencloud.common import exceptions, utils

from . import g, local_manager
from . import representations
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
        def make_response(data, code, headers=None):
            headers or {}
            resp = {'status': code}
            resp.update(data)
            return representations.to_json(resp, code, headers)

        if isinstance(err, exceptions.AuthenticationError):
            return make_response(
                {'message': 'Unauthorized'},
                401,
                {'WWW-Authenticate': 'Bearer realm="%s"' % self.app.name}
            )

        if isinstance(err, exceptions.AuthorizationError):
            return make_response({'message': 'Forbidden',}, 403)

        if isinstance(err, exceptions.InputError):
            return make_response(
                {
                    'message': 'Bad Request',
                    'errors': err.message
                }, 400
            )

        if isinstance(err, exceptions.ResourceMissingError):
            return make_response(
                {
                    'message': 'Not Found',
                    'errors': err.message
                }, 404
            )

        if isinstance(err, exceptions.UnprocessableError):
            return make_response(
                {
                    'message': 'Unprocessable Entity',
                    'errors': err.message
                }, 422
            )


        # Fall through to parent handler
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
    g.app = app
    g.api = api


    @app.before_request
    def attach_globals():
        """
        Attach useful, request-long, objects to the global g.
        """
        g.request = request

        g.connections = utils.Connections(
            redis=redis.client_factory(shared_pool=True),
            sql=sql.session_factory()
        )


    @app.teardown_request
    def cleanup(exc):
        """
        Ensure any used resources are cleaned up after the request.
        """
        if hasattr(g, 'connections') and hasattr(g.connections, 'sql'):
            if exc:
                g.connections.sql.rollback()
            g.connections.sql.close()


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
        token = _get_token_from_header(header)
        g.auth = authentication.lookup(g.connections, token)


    # Attach the api REST resource routes
    api.add_resource(resources.users.List, '/users')
    api.add_resource(resources.users.Item, '/users/<string:id>')
    api.add_resource(resources.accounts.List, '/accounts')
    api.add_resource(resources.accounts.Item, '/accounts/<string:id>')

    # Attach the api action routes (not necessarily RESTy)
    api.add_resource(actions.users.Login, '/users/login')
    api.add_resource(actions.tokens.Verify, '/tokens/verify')
    api.add_resource(actions.tokens.SubHub, '/tokens/subhub')

    # Attach non-api routes
    app.register_blueprint(views.health.bp, url_prefix='/health')

    # Werkzeug middleware to ensure a clean 'g' object per request.
    app.wsgi_app = local_manager.make_middleware(app.wsgi_app)

    return app.wsgi_app



def _get_token_from_header(header):
    """
    Inspect the given header value and retrieve the token from it.

    Returns:
        The token string.
    Raises:
        AuthenticationError.
    """
    if not header:
        raise exceptions.AuthenticationError('Bad Header')
    splits = header.split()
    if len(splits) != 2:
        raise exceptions.AuthenticationError('Bad Header')
    auth_type, token = splits
    if auth_type != 'Bearer':
        raise exceptions.AuthenticationError('Bad Header')
    return token

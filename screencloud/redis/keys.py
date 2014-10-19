"""
Helpers to construct redis keys.
"""

PREFIX = 'router-api/'
AUTHENTICATION_TOKEN = PREFIX+'auth/tokens/%s'

def authentication_token(token):
    return AUTHENTICATION_TOKEN % token

"""
Helpers to construct redis keys.
"""

AUTHENTICATION_TOKEN = 'authentication/tokens/%s'

def authentication_token(token):
    return AUTHENTICATION_TOKEN % token

"""
Helpers to construct redis keys.
"""

PREFIX = 'router-api/'
AUTHENTICATION_TOKEN = PREFIX+'auth/tokens/%s'
SCREEN_TICKET = PREFIX+'screens/tickets/%s'

def authentication_token(token):
    return AUTHENTICATION_TOKEN % token

def screen_ticket(ticket):
    return SCREEN_TICKET % ticket

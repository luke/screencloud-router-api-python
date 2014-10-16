class Error(Exception):
    """
    Base class for all errors in the app.
    """
    pass

class AuthenticationError(Error):
    pass

class AuthorizationError(Error):
    pass

class InputError(Error):
    pass

class ServiceUsageError(Error):
    """
    A method in the service layer has been called in an inappropriate way.
    """
    pass

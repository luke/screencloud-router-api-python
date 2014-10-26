import schematics.exceptions

class Error(Exception):
    """
    Base class for all errors in the app.

    We inherit from schematics errors as an easy way to provide feedback by
    passing in a dict of messages.
    """
    pass

class UserMessageError(Error):
    """
    Base class for errors with user messages.

    It's excpeted user-safe feedback will be provided by passing in a JSON
    serializable object.  Ideally a dict of messages.
    """
    pass

class AuthenticationError(Error):
    pass

class AuthorizationError(Error):
    pass

class InputError(UserMessageError):
    """
    Bad data was supplied.

    User-safe feedback should be provided.
    """
    pass

class UnprocessableError(UserMessageError):
    """
    An action could not be performed due to internal constraints.

    User-safe feedback should be provided.
    """
    pass

class ResourceMissingError(UserMessageError):
    """
    The primary resource relating to the action does not exist.

    User-safe feedback be should provided.
    """
    pass

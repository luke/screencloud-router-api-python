import schematics.exceptions

from screencloud.common import exceptions

def validate_input_structure(request, scheme):
    """
    Helper to validate input data.

    `scheme` should be a schematics model (inherited from
    `screencloud.api.schemas.Model`).

    Returns:
        The validated input data as an instance of 'scheme'.
    Raises:
        InputError.
    """
    try:
        data = scheme(request.get_json())
        data.validate()
    except schematics.exceptions.BaseError as exc:
        raise exceptions.InputError(exc.message)
    return data

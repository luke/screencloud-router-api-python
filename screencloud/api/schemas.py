from schematics.models import Model as BaseModel
from schematics.types import StringType, DateTimeType, EmailType
from schematics.types.compound import ModelType, DictType, ListType
from schematics.transforms import whitelist, blacklist
import schematics.exceptions

from screencloud.common import exceptions


class Model(BaseModel):
    """Our version of the ``schematics.model.Model``.

    This just allows us to default `strict=False` on validation so that we can
    ignore rogue fields posted through to the api.
    """

    def __init__(self, raw_data=None, deserialize_mapping=None, strict=False):
        return super(Model, self).__init__(raw_data, deserialize_mapping, strict)


class HalModel(Model):
    """Instances of HalModel should be capable of being represented in
    application/hal+json form.

    See ``screencloud.api.representations``
    """
    pass



class IdentityInput(Model):
    identifier = StringType(required=True)
    type = StringType(required=True)
    data = DictType(StringType(), required=True)


class UserInput(Model):
    name = StringType(required=True)
    email = EmailType(required=True)


class AuthResponse(HalModel):
    token = StringType()
    scopes = ListType(StringType())


class UserResponse(HalModel):
    id = StringType()
    name = StringType()
    email = EmailType()



def validate_input_structure(request, scheme, partial=False):
    """
    Helper to validate input data.

    `scheme` should be a schematics model (inherited from
    `screencloud.api.schemas.Model`).

    For doing PATCH requests, partial=True should be used to allow partial data
    to pass validation.

    Returns:
        The validated input data as an instance of 'scheme'.
    Raises:
        InputError.
    """
    try:
        data = scheme(request.get_json())
        data.validate(partial=partial)
    except schematics.exceptions.BaseError as exc:
        raise exceptions.InputError(exc.message)
    return data

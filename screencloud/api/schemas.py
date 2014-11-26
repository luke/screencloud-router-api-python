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

    Also adds the `from_object` class method to help convert model objects
    returned from the service layer to schematics models for output.
    """

    def __init__(self, raw_data=None, deserialize_mapping=None, strict=False):
        return super(Model, self).__init__(raw_data, deserialize_mapping, strict)

    @classmethod
    def from_object(cls, obj, initial_data=None):
        """
        Convert an arbitrary object (with appropriately named attributes) into
        instances of this class.

        Uses `getattr` to read values from the model.
        """
        def field_to_value(field, obj_val):
            if isinstance(field, ModelType):
                return field.model_class.from_object(obj_val)
            else:
                return obj_val

        data = initial_data or {}

        for name, field in cls.fields.items():
            if name in data:
                continue

            obj_attr = getattr(obj, name)

            if isinstance(field, ListType):
                inner_field = field.field
                data[name] = [
                    field_to_value(inner_field, val) for val in obj_attr
                ]
            else:
                data[name] = field_to_value(field, obj_attr)

        return cls(data)


class HalModel(Model):
    """Instances of HalModel should be capable of being represented in
    application/hal+json form.

    See ``screencloud.api.representations``
    """
    pass



class IdentityInput(Model):
    """
    Generic Identity data.  Best to use specific ones.
    """
    identifier = StringType(required=True)
    type = StringType(required=True)
    data = DictType(StringType(), required=True)

class NetworkIdentityInput(Model):
    """
    Identity tied to a specific top-level network.

    Will use the basic-namespaced identity type, with the namespace being the
    network_id of the top-level network this request is being performed under.

    The only data needed from the user/comsumer-app is the identifier and a
    secret.
    """
    identifier = StringType(required=True)
    secret = StringType(required=True)


class UserInput(Model):
    name = StringType(required=True)
    email = EmailType(required=True)

class AccountInput(Model):
    name = StringType(required=True)


class AuthResponse(HalModel):
    token = StringType()
    scopes = ListType(StringType())

class NetworkResponse(HalModel):
    id = StringType()
    name = StringType()

class AccountResponse(HalModel):
    id = StringType()
    name = StringType()
    networks = ListType(ModelType(NetworkResponse))

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

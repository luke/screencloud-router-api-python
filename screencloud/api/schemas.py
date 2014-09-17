from schematics.models import Model as BaseModel
from schematics.types import StringType, DateTimeType
from schematics.transforms import whitelist, blacklist


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


class Account(HalModel):
    id = StringType()
    name = StringType(required=True)
    created_at = DateTimeType()

    class Options:
        roles = {
            'post': whitelist('name'),
            'patch': whitelist('name'),
        }


class User(HalModel):
    id = StringType()
    name = StringType(required=True)
    created_at = DateTimeType()

    class Options:
        roles = {
            'post': whitelist('name'),
            'patch': whitelist('name'),
        }

from schematics.models import Model as BaseModel
from schematics.types import StringType, DateTimeType, EmailType
from schematics.types.compound import ModelType, DictType, ListType
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

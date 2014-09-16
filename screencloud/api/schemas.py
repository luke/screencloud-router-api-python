from schematics.models import Model as BaseModel
from schematics.types import StringType, DateTimeType


class Model(BaseModel):
    """Our version of the ``schematics.model.Model``.

    This just allows us to default `strict=False` on validation so that we can
    ignore rogue fields posted through to the api.
    """

    def __init__(self, raw_data=None, deserialize_mapping=None, strict=False):
        return super(Model, self).__init__(raw_data, deserialize_mapping, strict)


class Account(Model):
    id = StringType()
    name = StringType(required=True)
    created_at = DateTimeType()

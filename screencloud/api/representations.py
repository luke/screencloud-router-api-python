import json

from flask import make_response

from . import schemas

def to_json(data, code, headers=None):
    dumped = json.dumps(data, indent=2, default=_serializer_extensions) + '\n'
    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp


# TODO:
def to_hal_json(data, code, headers=None):
    raise NotImplementedError('hal+json representation')


def _serializer_extensions(obj):
    # Serialize our schemas
    if isinstance(obj, schemas.Model):
        return obj.to_primitive()

import json

from flask import make_response

from . import schemas

def to_json(data, code, headers=None):
    if isinstance(data, schemas.Model):
        data = data.to_primitive()

    dumped = json.dumps(data, indent=2, sort_keys=False) + '\n'
    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp


# TODO:
def to_hal_json(data, code, headers=None):
    raise NotImplementedError('hal+json representation')

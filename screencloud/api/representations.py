import json

from flask import make_response

from . import schemas

def to_json(data, code, headers=None):
    dumped = json.dumps(data, indent=2, cls=JsonEncoder) + '\n'
    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp


# TODO:
def to_hal_json(data, code, headers=None):
    raise NotImplementedError('hal+json representation')



class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        # Serialize our schemas
        if isinstance(obj, schemas.Model):
            return obj.to_primitive()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

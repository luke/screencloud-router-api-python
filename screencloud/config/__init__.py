from . import default, local

import logging

def to_dict():
    d_obj = {k:v for k,v in default.__dict__.items() if not k.startswith('__')}
    l_obj = {k:v for k,v in local.__dict__.items() if not k.startswith('__')}
    obj = dict()
    obj.update(d_obj)
    obj.update(l_obj)
    return obj

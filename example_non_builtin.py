import sys


sys.policy = {
    'socket': [],
}

default = __import__


def overriden_import_func(*args, **kwargs):
    module = default(*args, **kwargs)
    return module


__import__ = overriden_import_func
import requests

print('done')

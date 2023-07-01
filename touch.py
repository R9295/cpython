import socket
from functools import wraps
from contextlib import contextmanager

url = 'github.com'

def request(obj, perm):
    obj.allowed.append(perm)
    print('granted: '+perm)

def revoke(obj, perm):
    obj.allowed.remove(perm)
    print('revoked: '+perm)


@contextmanager
def request_ctx(*args, **kwds):
    request(args[0], args[1])
    try:
        yield
    finally:
        revoke(args[0], args[1])

sk = socket.socket()
try:
    sk.connect((url, 80))
except SystemError as e:
    print(e)

request(sk,url)
sk.connect((url, 80))
revoke(sk, url)
sk.close()

sk = socket.socket()
with request_ctx(sk, url):
    sk.connect((url, 80))

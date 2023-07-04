import socket


permit 'codeberg.org':
    s = socket.socket()
    s.connect(('codeberg.org', 80))
    try:
        d = socket.socket()
        d.connect(('github.com', 80))
        raise Exception('Did not error')
    except SystemError as e:
        pass
    permit 'google.com':
        # allows for nested permits. It will stack the permit values.
        b = socket.socket()
        b.connect(('google.com', 80))

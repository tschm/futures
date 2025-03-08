from collections import namedtuple
from contextlib import contextmanager

import blpapi
import numpy as np
from blpapi import AuthOptions

# Tuple describing the parameter required to establish a connection
Connection = namedtuple("Connection", ["app_name", "server_host", "server_port"])

# The connection for our internal bpipe
bpipe = Connection(
    app_name="...",
    server_host="...",
    server_port=8194,
)


@contextmanager
def connect(connection=None):
    """
    Yields a session for Bloomberg, will stop it once it has been used

    referecing to blpapi example for full lists of available authentication methods:
        https://github.com/msitt/blpapi-python/blob/master/examples/ConnectionAndAuthExample.py
    """

    connection = connection or bpipe
    auth = AuthOptions.createWithApp(connection.app_name)
    options = blpapi.SessionOptions()
    options.setServerHost(connection.server_host)
    options.setServerPort(connection.server_port)
    options.setSessionIdentityOptions(auth)
    options.maxEvents = np.inf

    session = blpapi.Session(options)
    session.start()

    yield session
    session.stop()

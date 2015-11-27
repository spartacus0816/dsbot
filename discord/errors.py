# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2015 Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

try:
    import http.client as httplib
except ImportError:
    import httplib

class DiscordException(Exception):
    """Base exception class for discord.py

    Ideally speaking, this could be caught to handle any exceptions thrown from this library.
    """
    pass

class ClientException(DiscordException):
    """Exception that's thrown when an operation in the :class:`Client` fails.

    These are usually for exceptions that happened due to user input.
    """
    pass

class GatewayNotFound(DiscordException):
    """An exception that is usually thrown when the gateway hub
    for the :class:`Client` websocket is not found."""
    def __init__(self):
        message = 'The gateway to connect to discord was not found.'
        super(GatewayNotFound, self).__init__(message)

class HTTPException(DiscordException):
    """Exception that's thrown when an HTTP request operation fails.

    .. attribute:: response

        The response of the failed HTTP request. This is an
        instance of `requests.Response`__.

        __ http://docs.python-requests.org/en/latest/api/#requests.Response
    """

    def __init__(self, response, message=None):
        self.response = response

        if message is None:
            message = httplib.responses.get(response.status_code, 'HTTP error')

        message = '{0} (status code: {1.response.status_code})'.format(message, self)

        try:
            data = response.json()
            response_error = data['message']
            if response_error:
                message = '{}: {}'.format(message, response_error)
        except:
            pass

        super(HTTPException, self).__init__(message)

class InvalidArgument(ClientException):
    """Exception that's thrown when an argument to a function
    is invalid some way (e.g. wrong value or wrong type).

    This could be considered the analogous of ``ValueError`` and
    ``TypeError`` except derived from :exc:`ClientException` and thus
    :exc:`DiscordException`.
    """
    pass

class LoginFailure(ClientException):
    """Exception that's thrown when the :meth:`Client.login` function
    fails to log you in from improper credentials or some other misc.
    failure.
    """
    pass

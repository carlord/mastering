#! /usr/bin/env python
#==> part of the test followd by the wsgi tutorial
#    http://wsgi.tutorial.codepoint.net/environment-dictionary
# Python's bundled WSGI server
from wsgiref.simple_server import make_server

def application (environ, start_response):

    # Sorting and stringifying the environment key, value pairs
    response_body = [
        '%s: %s' % (key, value) for key, value in sorted(environ.items())
    ]
    response_body = '\n'.join(response_body)

    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(response_body)))
    ]
    start_response(status, response_headers)

    return [response_body]

# Instantiate the server
httpd = make_server ('localhost', 8051, application )

# Wait for a single request, serve it and quit
httpd.handle_request()


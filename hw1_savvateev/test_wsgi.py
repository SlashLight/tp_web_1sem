import urllib.parse
HELLO_WORLD = b"Hello world!\n"


def simple_app(environ, start_response):
    """Simplest possible application object"""
    resp = ''
    status = '200 OK'
    if environ['REQUEST_METHOD'] == 'GET':

        print("GET:", environ['QUERY_STRING'].split('&'))
    if environ['REQUEST_METHOD'] == 'POST':
        #resp = dict(urllib.parse.parse_qsl(
        #    environ['wsgi.input'].read(int(environ['CONTENT_LENGTH'])).decode())
        #)
        print("POST:", environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', '0'))).decode('utf-8').split('&'))

    response_headers = [('Content-type', 'text/plain')]
    return resp


application = simple_app

class AppClass:
    """Produce the same output, but using a class

    (Note: 'AppClass' is the "application" here, so calling it
    returns an instance of 'AppClass', which is then the iterable
    return value of the "application callable" as required by
    the spec.

    If we wanted to use *instances* of 'AppClass' as application
    objects instead, we would have to implement a '__call__'
    method, which would be invoked to execute the application,
    and we would need to create an instance for use by the
    server or gateway.
    """

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield HELLO_WORLD

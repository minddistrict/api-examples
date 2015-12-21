# stdlib modules
import httplib
import json
import pprint
import sys
import time
import urlparse

# Local modules
import config


def pretty_print(var):
    pprint.pprint(var)


class InvalidAPICall(Exception):
    pass


class Connection(object):
    # Contextmanager for http connection.

    def __init__(self, url):
        parsed_url = urlparse.urlparse(url)
        self.port = self.get_port(parsed_url)
        self.hostname = parsed_url.hostname
        self.path = parsed_url.path

    def get_port(self, parsed_url):
        if parsed_url.port:
            return int(parsed_url.port)
        if parsed_url.scheme == 'https':
            return 443
        return 80

    def __enter__(self):
        self.connection = httplib.HTTPSConnection(self.hostname, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def send_call(self, method, headers, body):
        self.connection.request(
            method=method,
            url=self.path,
            body=body,
            headers=headers)

    @property
    def response(self):
        return self.connection.getresponse()


class APICaller(object):

    def __init__(self, url, data, method):
        self.url = url
        self.data = data
        self.method = method
        self.headers = self.get_headers()
        self.body = self.get_body()
        self.result = None

    def get_headers(self):
        headers = {'Accept': 'application/json'}
        headers['Authorization'] = 'md-token ' + config.token
        if self.data:
            headers['Content-Type'] = 'application/json'
        return headers

    def get_body(self):
        return json.dumps(self.data) if self.data else None

    def wait_between_calls(self):
        time.sleep(config.wait_between_requests)

    def check_response_for_invalid(self):
        if self.response.status not in [200, 201, 204]:
            raise InvalidAPICall(
                "Error while querying the API:\n",
                "Method: {}\n".format(self.method),
                "URL: {}\n".format(self.url),
                "Body: {}\n".format(self.response.read()))

    def process_response(self):
        self.check_response_for_invalid()
        # A 204 doesn't return any data.
        if self.response.status != 204:
            self.result = json.loads(self.response.read())

    def debug_input(self):
        print '\n', 40 * '-'
        print "INPUT"
        print "url: {}".format(self.url)
        print "method: {}".format(self.method)
        print "data:"
        pretty_print(self.data)
        print "headers:"
        pretty_print(self.headers)
        print "body:"
        pretty_print(self.body)

    def debug_output(self):
        print '\n', 40 * '-'
        print "OUTPUT"
        print "status: {}".format(self.response.status)
        print "result:"
        pretty_print(self.result)

    def __call__(self):
        self.wait_between_calls()
        if config.debug:
            self.debug_input()
        with Connection(self.url) as connection:
            connection.send_call(self.method, self.headers, self.body)
            self.response = connection.response
            self.process_response()
        if config.debug:
            self.debug_output()
        return self.result


def query_api(url, data=None, method='GET'):
    # Thin wrapper around APICaller.
    try:
        return APICaller(url, data, method)()
    except InvalidAPICall as error:
        sys.exit(error)

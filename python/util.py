import json
import httplib
import urlparse
import sys


def get_port_number(info):
    """Return the correct port number to query.
    """
    if info.port:
        return int(info.port)
    if info.scheme == 'https':
        return 443
    return 80


def query_api(url, data=None, token=None, method='GET'):
    """Query a specific endpoint in the API.
    """
    info = urlparse.urlparse(url)
    connection = httplib.HTTPSConnection(info.hostname, get_port_number(info))
    body = None
    headers = {'Accept': 'application/json'}
    if token:
        headers['Authorization'] = 'md-token ' + token
    if data:
        body = json.dumps(data)
        headers['Content-Type'] = 'application/json'
    connection.request(
        method=method, url=info.path, body=body, headers=headers)
    response = connection.getresponse()
    if response.status not in [200, 201, 204]:
        print 'Error while querying the API:'
        print 'Method:', method
        print 'URL:', url
        print 'Body:', response.read()
        sys.exit(1)
    if response.status == 204:
        # 204 doesn't return any data.
        result = None
    else:
        result = json.loads(response.read())
    connection.close()
    return result

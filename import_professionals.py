#!/usr/bin/env python
"""This script uses the Minddistrict API in order to add
professionals from an CSV file.
"""
import argparse
import csv
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
    connection = httplib.HTTPConnection(info.hostname, get_port_number(info))
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


def get_api_token(url, login, password):
    """Retrieve a token out of the API.
    """
    authenticate_url = url + '/authenticate'
    result = query_api(
        url=authenticate_url,
        data={"login": login,
              "password": password,
              "id": "inport_clients.py",
              "description": "Import clients API example"},
        method='POST')
    return result['token']


ROLE_MAP = {
    'secretary': 'ith.Secretary',
    'therapist': 'ith.Therapist',
    'supervisor': 'ith.Supervisor',
    'application manager': 'ith.ApplicationManager',
    'analyst': 'ith.Analyst'
}


def read_csv(path):
    """Read the CSV file returning professional information as Python
    dictionaries.
    """
    professionals = []
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        reader.next()  # Skip the first "header" row.
        for row in reader:
            professionals.append({
                'email': row[0].strip(),
                'id': row[1].strip(),
                'first_name': unicode(row[2], "UTF-8").strip(),
                'infix': unicode(row[3], "UTF-8").strip(),
                'last_name': unicode(row[4], "UTF-8").strip(),
                'role': ROLE_MAP[row[5].strip().lower()],
            })
    return professionals


def add_professionals(professionals, url, token):
    """Add the list of professional using the API at URL and the given token.
    """
    professionals_url = url + '/p'

    for professional in professionals:
        print 'Create', professional["email"]
        # Create the professional
        result = query_api(
            url=professionals_url,
            data={"email": professional["email"],
                  "id": professional["id"],
                  "first_name": professional["first_name"],
                  "infix": professional["infix"],
                  "last_name": professional["last_name"],
                  "active": True},
            token=token,
            method='POST')
        # Set the role of the professional
        professional_url = result['@url'] + '/roles'
        result = query_api(
            url=professional_url,
            data={"roles": [professional["role"]]},
            token=token,
            method='PATCH')


def csv_to_professional_import():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'login',
        help=('Login to use'))
    parser.add_argument(
        'password',
        help=('Password to use'))
    parser.add_argument(
        'url',
        help=('API Base url.'))
    parser.add_argument(
        'path',
        help=('The path to the csv file.'))

    args = parser.parse_args()
    professionals = read_csv(args.path)
    token = get_api_token(args.url, args.login, args.password)
    add_professionals(professionals, args.url, token)

if __name__ == '__main__':
    csv_to_professional_import()

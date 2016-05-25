#!/usr/bin/env python
"""This script uses the Minddistrict API in order to add
professionals from an CSV file.
"""
import csv
import util
import config

ROLE_MAP = {
    'secretary': 'ith.Secretary',
    'therapist': 'ith.Therapist',
    'supervisor': 'ith.Supervisor',
    'application manager': 'ith.ApplicationManager',
    'analyst': 'ith.Analyst'
}


def get_professionals_to_import(path):
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


class Professional(object):

    def __init__(self, email, id, first_name, infix, last_name):
        self.professionals_url = config.url + '/p'
        self.email = email
        self.id = id
        self.first_name = first_name
        self.infix = infix
        self.last_name = last_name

    def create(self):
        print 'Create', self.email
        # TODO Raise error if problem.
        result = util.query_api(
            url=self.professionals_url,
            data={
                "email": self.email,
                "id": self.id,
                "first_name": self.first_name,
                "infix": self.infix,
                "last_name": self.last_name,
                "active": True},
            token=config.token,
            method='POST')
        self.url = result['@url']

    def set_role(self, role):
        url = self.url + '/roles'
        return util.query_api(
            url=url,
            data={"roles": [role]},
            token=config.token,
            method='PATCH')


def add_professionals(professionals, url, token):
    for professional_info in professionals:
        prof = Professional(
            professional_info['email'],
            professional_info['id'],
            professional_info['first_name'],
            professional_info['infix'],
            professional_info['last_name']
        )
        prof.create()
        prof.set_role(professional_info['role'])


if __name__ == '__main__':
    add_professionals(
        get_professionals_to_import(config.path),
        config.url,
        config.token)
    print "done"

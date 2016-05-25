"""
Some error handling around the queries would be nice.
"""
import util
import tasks


class Professional(object):

    def __init__(self, professional_result):
        # professional_result contains what the API returns
        self.url = professional_result['@url']
        # Attributes that all professionals have.
        self.email = professional_result['email']
        self.active = professional_result['active']
        self.first_name = professional_result['first_name']
        self.infix = professional_result['infix']
        self.last_name = professional_result['last_name']

        # Attributes that professionals *may* have.
        # Depends on application configuration.
        self.id = professional_result.get('id')

    def get_tasks(self):
        result = util.query_api(url=self.url + '/tasks/items', method='GET')
        for task_result in result['@items']:
            yield tasks.Task(task_result)

    def set_role(self, role):
        util.query_api(
            url=self.url + '/roles',
            data={"roles": [role]},
            method='PATCH')


class Professionals(object):

    def __init__(self, url):
        self.base_url = url
        self.url = url + '/p'

    def create_professional(self, id, email, first_name, infix, last_name):
        util.query_api(
            url=self.url,
            method='POST',
            data={
                "id": id,
                "email": email,
                "active": True,
                "first_name": first_name,
                "infix": infix,
                "last_name": last_name})
        print "Added professional {}".format(email)

    def get_all_professionals(self):
        result = util.query_api(url=self.url + '/items', method='GET')
        for professional_result in result['@items']:
            yield Professional(professional_result)

    def get_by_id(self, id):
        return Professional(util.query_api(
            url=self.base_url + '/aux/professional/id/{}'.format(id),
            method='GET'))

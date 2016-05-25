"""
Some error handling around the queries would be nice.
"""
import util
import tasks


class Client(object):

    def __init__(self, client_result):
        # client_result contains what the API returns
        self.url = client_result['@url']
        # Attributes that all clients have.
        self.email = client_result['email']
        self.active = client_result['active']
        self.gender = client_result['gender']

        # Attributes that clients *may* have. Clients can be anonymous and
        # they may or may not have an id, depending on the app configuration.
        self.id = client_result.get('id')
        self.first_name = client_result.get('first_name')
        self.infix = client_result.get('infix')
        self.last_name = client_result.get('last_name')
        self.date_of_birth = client_result.get('date_of_birth')
        self.age = client_result.get('age')
        self.nickname = client_result.get('nickname')

    def get_tasks(self):
        result = util.query_api(url=self.url + '/tasks/items', method='GET')
        for task_result in result['@items']:
            yield tasks.Task(task_result)


class Clients(object):

    def __init__(self, url):
        self.base_url = url
        self.url = url + '/c'

    def create_client(
            self, id, email, first_name, infix, last_name, gender,
            date_of_birth):
        util.query_api(
            url=self.url,
            method='POST',
            data={
                "id": "{}".format(id),
                "email": email,
                "active": True,
                "first_name": first_name,
                "infix": infix,
                "last_name": last_name,
                "date_of_birth": date_of_birth,
                "gender": gender})
        print "Added client {}".format(email)

    def get_all_clients(self):
        result = util.query_api(url=self.url + '/items', method='GET')
        for client_result in result['@items']:
            yield Client(client_result)

    def get_by_id(self, id):
        return Client(util.query_api(
            url=self.base_url + '/aux/client/id/{}'.format(id),
            method='GET'))

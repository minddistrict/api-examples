"""
Starting point for demos of the Minddistrict REST API endpoints.
"""
# stdlib imports
import argparse
import inspect
import csv

# local imports
import clients
import config
import professionals
import random_data


def list_clients():
    """
    For all clients, list some of their attributes.
    """
    for client in clients.Clients(config.url).get_all_clients():
        print client.id, client.email, client.first_name


def show_client_tasks():
    """
    For a certain client list all their tasks.
    ID is hardcoded in the constant.
    """
    CLIENT_ID = 123
    client = clients.Clients(config.url).get_by_id(CLIENT_ID)
    print "Tasks for {}:".format(client.email)
    tasks = client.get_tasks()
    for task in tasks:
        print task.title
        print task.url
        print task.creation_time
        print task.message


def add_random_client():
    client_factory = clients.Clients(config.url)
    first_name = random_data.first_name()
    infix = random_data.infix()
    last_name = random_data.last_name()
    email = random_data.email(first_name, infix, last_name)
    client_factory.create_client(
        random_data.id(),
        email,
        first_name,
        infix,
        last_name,
        random_data.gender(),
        random_data.date_of_birth())


def add_random_clients():
    """
    Add a number of clients with random data.
    """
    NUMBER_OF_CLIENTS_TO_ADD = 10
    for _ in range(NUMBER_OF_CLIENTS_TO_ADD):
        add_random_client()


def list_professionals():
    """
    For all professionals, list some of their attributes.
    """
    for professional in professionals.Professionals(
            config.url).get_all_professionals():
        print professional.id, professional.email, professional.first_name


def show_professional_tasks():
    """
    For a certain professional list all their tasks.
    ID is hardcoded in the constant.
    """
    PROFESSIONAL_ID = 'abc'
    professional = professionals.Professionals(
        config.url).get_by_id(PROFESSIONAL_ID)
    print "Tasks for {}:".format(professional.email)
    tasks = professional.get_tasks()
    for task in tasks:
        print task.title
        print task.url
        print task.creation_time
        print task.message


ROLE_MAP = {
    'secretary': 'ith.Secretary',
    'therapist': 'ith.Therapist',
    'supervisor': 'ith.Supervisor',
    'application manager': 'ith.ApplicationManager',
    'analyst': 'ith.Analyst'
}


def _get_professionals_to_import(path):
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


def import_professionals_from_csv():
    """
    Import the professionals in the csv file.
    """
    CSV_PATH = 'professionals.csv'
    profs = professionals.Professionals(config.url)
    for professional_info in _get_professionals_to_import(CSV_PATH):
        profs.create_professional(
            professional_info['id'],
            professional_info['email'],
            professional_info['first_name'],
            professional_info['infix'],
            professional_info['last_name'])
        profs.get_by_id(
            professional_info['id']).set_role(
                professional_info['role'])


def _get_possible_commands():
    return dict(
        (name, a_global) for (name, a_global) in globals().items()
        if inspect.isfunction(a_global) and not name.startswith('_')
    )


def _get_command_given(commands):
    parser = argparse.ArgumentParser(
        description='What do you want to do today?')
    parser.add_argument('command', choices=sorted(commands.keys()))
    args = parser.parse_args()
    return args.command

if __name__ == '__main__':
    commands = _get_possible_commands()
    command = _get_command_given(commands)
    commands[command]()

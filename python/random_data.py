import random


def first_name():
    return random.choice([
        "Jack",
        "John",
        "Fred",
        "Simone",
        "Anne",
        "Eve"
    ])


def infix():
    return random.choice([
        "",
        "the",
        "of",
        "von"
    ])


def last_name():
    return random.choice([
        "Bauer",
        "Astaire",
        "Woo",
        "Bovarie",
        "Fredricks",
        "Gutmans"
    ])


def id():
    return random.randint(1000, 10000)


def email(first_name, infix, last_name):
    email = ''
    email += first_name.lower()
    if infix:
        email += '.' + infix.lower()
    email += '.' + last_name.lower()
    email += '@' + random.choice([
        "example.com",
        "example.org",
        "example.foo",
        "example.bar",
        "example.qux"
    ])
    return email


def date_of_birth():
    year = random.randint(1900, 2013)
    month = '{0:02d}'.format(random.randint(1, 12))
    day = '{0:02d}'.format(random.randint(1, 28))
    return "{}-{}-{}".format(year, month, day)


def gender():
    return random.choice(["m", "f"])

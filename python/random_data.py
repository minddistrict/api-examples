import random


def first_name():
    return random.choice([
        "Jack",
        "John",
        "Fred",
        "Simone",
        "Anne",
        "Eve",
        "Marie",
        "Marty",
        "Jill",
        "George",
        "Danny",
        "Eugene"
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
        "Gutmans",
        "Zuckerberg",
        "Breisenstein",
        "Johnson",
        "Jackson",
        "Oldway",
        "McFly",
        "Tannen"
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


"""
If the burgerservicenummer is ABCDEFGHI then the following must be divisible
by 11.
(9 x A) + (8 x B) + (7 x C) + (6 x D) + (5 x E) + (4 x F) + (3 x G) + (2 x H) + (-1 x I)
"""
_bsnweights = (9, 8, 7, 6, 5, 4, 3, 2, -1)


def _bsn_eleven_test(bsn):
    # As per: http://nl.wikipedia.org/wiki/BSN#11-proef
    #
    # for ABCDEFGHI:
    #
    # (9 x A) + (8 x B) + (7 x C) + (6 x D) + (5 x E) + (4 x F) +
    # (3 x G) + (2 x H) + (-1 x I) % 0 == 0
    #
    # BSNs with length 8 will be left padded with a '0'.
    #
    try:
        bsn = str(bsn)
    except ValueError:
        return False
    if not 7 < len(bsn) < 10:
        return False
    bsn = bsn.rjust(9, '0')
    total = 0
    for weight, item in zip(_bsnweights, bsn):
        try:
            item = int(item)
        except ValueError:
            return False
        total += item * weight
    if total % 11:
        # Cannot be cleanly divided by 11, so not valid.
        return False
    return True

def bsn():
    # Seems like a wasteful process but it's all numbers so easy on the CPU.
    while True:
        bsn_list_incomplete = [str(random.randint(0,9)) for _ in range(8)]
        for i in range(10):
            bsn = "".join(bsn_list_incomplete + [str(i)])
            if _bsn_eleven_test(bsn):
                return bsn

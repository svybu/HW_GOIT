import json


def write_contacts_to_file(filename, contacts):
    with open(filename, 'w') as fh:
        r = {"contacts":contacts}
        json.dump(r, fh)

def read_contacts_from_file(filename):
    with open(filename, 'r') as fh:
        r  = json.load( fh)
        contacts = r['contacts']
        return contacts




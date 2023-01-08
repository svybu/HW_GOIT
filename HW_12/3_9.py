import csv


def write_contacts_to_file(filename, contacts):
    with open(filename, 'w', newline=''):
        head = ["name","email","phone","favorite"]
        r = csv.DictWriter(contacts, fieldnames=head)
        r.writeheader()
        r.writerow(contacts)

def read_contacts_from_file(filename):
    with open(filename, 'r', newline=''):
        r = csv.DictReader(filename)
        return r

contacts = [  {
    "name": "Allen Raymond",
    "email": "nulla.ante@vestibul.co.uk",
    "phone": "(992) 914-3792",
    "favorite": False
}]
write_contacts_to_file('/Users/sviatslav/Desktop/python/GOIT/HW_GOIT/HW_GOIT/123', contacts)







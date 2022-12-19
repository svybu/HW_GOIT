from collections import UserDict

class AdressBook(UserDict):


    def add_record(self, Record):
        self[Record.name.value] = Record



class Record():
    def __init__(self, name, phone = None):
        self.name = Name(name)
        self.phone = []
        if phone:
            self.phone.append(Phone(phone))

    def add__phone(self, phone):
        self.phone.append(Phone(phone))

    def remove_phone(self, phone):
        self.phone.remove(phone)

    def change_phone(self, phone, new_phone):
        self.phone[self.phone.index(phone)] = new_phone

class Field():
    pass

class Name(Field):
    def __init__(self, name):
        self.value = name


class Phone(Field):
    def __init__(self, phone = None):
        self.value = phone

a = AdressBook()

b = Record('asdwdas', '1234')
a.add_record(b)
print(a)
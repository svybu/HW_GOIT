from collections import UserDict
import datetime
import re

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'No contact with this name, try again'
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return 'This contact exists already, try again'
        except TypeError as exception:
            return "Sorry, I didn't understand this command, please try again"

    return inner


class AdressBook(UserDict):

    @input_error
    def add_record(self, record):
        self[record.name.value] = record

    def iterator(self, count=2):
        page = []
        i = 0
        for record in self.data.values():
            page.append(record)
            i += 1
            if i == count:
                yield page
                page = []
                i = 0
        if page:
            yield page


class Record():
    def __init__(self, name, phone=[], birthday = None):
        self.name = Name(name)
        self.phone = []
        if birthday:
            self.birthday = Birthday(birthday)
        else:
            self.birthday = None
        if phone:
            self.add_phone(phone)

    @input_error
    def days_to_bd(self):
        now = datetime.datetime.today()
        birthday = self.birthday.value
        #print(birthday)
        birthday = datetime.datetime.strptime(birthday, '%d.%m.%Y')
        b_d = datetime.datetime(now.year, birthday.month, birthday.day)
        days = b_d - now
        if b_d < now:
            b_d = datetime.datetime(now.year + 1, birthday.month, birthday.day)
            days = b_d - now
        days = days.days
        if days == 0:
            days = 'This person has birthday today'
        return days

    @input_error
    def add_phone(self, phone):
        self.phone.append(Phone(phone))

    @input_error
    def remove_phone(self, phone):
        self.phone.remove(phone)

    @input_error
    def change_phone(self, new_phone):
        self.phone.clear()
        self.phone.append(Phone(new_phone))

    def get_data(self):
        phones_data = ''
        birthday_data = ''
        for phone in self.phone:
            phones_data += f'{phone.value}, '
        if self.birthday:
            birthday_data = f' Birthday : {self.birthday.value}'

        return f'{self.name.value} : {phones_data[:-2], birthday_data}'


class Field():
    pass

class Name(Field):
    def __init__(self, name):
        self.__value = name

    @property
    def value(self):
        return self.__value

class Phone(Field):
    def __init__(self, phone = None):
        self.__value = None
        self.value = phone

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, phone):
        if phone.isnumeric():
            self.__value=phone
        else:
            print('only numbers allowed in phone')

class Birthday(Field):
    def __init__(self, birthday):
        self.__value = None
        self.value = birthday

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, birthday):
        #if  self.__value==re.fullmatch('\d{2}[.]\d{2}[.]\d{4}',birthday):
            #self.__value = birthday
        now = datetime.datetime.now()
        birth_day = datetime.datetime.strptime(birthday,'%d.%m.%Y').date()
        if birth_day> now.date():
            raise ValueError('birthdate must be less then the date today')
        else:
            self.__value = birthday

contacts = AdressBook()


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'No contact with this name, try again'
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return 'This contact exists already, try again'
        except TypeError as exception:
            return "Sorry, I didn't understand this command, please try again"

    return inner


@input_error
def add_contact(args):
    if len(args) == 3:
        name, phone, birthday = args
        if name in contacts.keys():
            raise ValueError('This contact is in memory')
        record = Record(name, phone, birthday)
        contacts.add_record(record)
    else:
        name, phone = args
        if name in contacts.keys():
            raise ValueError('This contact is in memory')
        record = Record(name, phone)
        contacts.add_record(record)
    return f'{name} added as contact'


@input_error
def change_contact(args):
    name, phone = args
    if name in contacts.keys():
        contacts[name].change_phone(phone)
    return f'{name} phone changed to {phone}'


@input_error
def show_chosen(args):
    name = args[0]
    for i in contacts[name].phone:
        phone = i.value
        return f'{name} phone is {phone}'


@input_error
def show_all(a):
    result = ''
    i = 1
    for page in contacts.iterator():
        result +=f'Page{i}\n'
        for record in page:
            result +=f'{record.get_data()}\n'
        i+=1
    return result


def wrong_command():
    return 'Wrong command('


@input_error
def hello(a):
    return 'How can I help you?'


def exit(a):
    return "Good bye!"

def days_to_birthday(args):
    name= args[0]
    days = Record.days_to_bd(contacts[name])
    return f"There are {days} days to {name}'s birthday"


HANDLERS = {"hello": hello,
            "add": add_contact,
            'change': change_contact,
            'phone': show_chosen,
            'show all': show_all,
            'good bye': exit,
            'close': exit,
            'exit': exit,
            '.': exit,
            'костиль': wrong_command,
            'birthday': days_to_birthday
            }


@input_error
def parser_string(u_input):
    command, *args = u_input.split()
    if args:
        if ((command + ' ' + args[0]).lower()) in ['show all', 'good bye']:
            command = (command + ' ' + args[0]).lower()
        handler = HANDLERS.get(command.lower(), wrong_command())
    else:
        handler = HANDLERS.get(command.lower(), wrong_command())
    return handler, args


@input_error
def main():
    while True:
        u_input = input('Enter command ')
        handler, *args = parser_string(u_input)
        if handler == wrong_command():
            print(handler)
        elif handler == exit:
            print("Good bye!")
            break
        else:
            result = handler(*args)
            print(result)

if __name__ == '__main__':
    main()

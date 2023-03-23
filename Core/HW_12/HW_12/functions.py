from decorator import input_error
from classes import contacts, Record


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
        result += f'Page{i}\n'
        for record in page:
            result += f'{record.get_data()}\n'
        i += 1
    return result


def wrong_command():
    return 'Wrong command('


@input_error
def hello(a):
    return 'How can I help you?'


def exit(a):
    # contacts.save_contacts_to_file()
    return "Good bye!"


def days_to_birthday(args):
    name = args[0]
    days = Record.days_to_bd(contacts[name])
    return f"There are {days} days to {name}'s birthday"


def search(value):
    result = ''
    records = contacts.search(value)
    print(records)
    for i in records:
        print(i)
        result += f'{i.get_data()}\n'
    return result


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
            'birthday': days_to_birthday,
            'search': search
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

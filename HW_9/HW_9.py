
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
    name, phone = args
    if name in contacts.keys():
        raise ValueError('This contact is in memory')
    contacts[name] = phone
    return f'{name} added as contact'


@input_error
def change_contact(args):
    name, phone = args
    if name in contacts.keys():
        contacts[name] = phone
    return f'{name} phone changed to {phone}'


@input_error
def show_chosen(args):
    name = args[0]
    phone = contacts[name]
    return f'{name} phone is {phone}'


@input_error
def show_all(a):
    result_string = ''
    for name, phone in contacts.items():
        result_string = result_string + name + " phone is " + phone + '\n'
    return result_string

def wrong_command():
    return 'Wrong command('


@input_error
def hello(a):
    return 'How can I help you?'


def exit(a):
    return "Good bye!"


HANDLERS = {"hello": hello,
            "add": add_contact,
            'change': change_contact,
            'phone': show_chosen,
            'show all': show_all,
            'good bye': exit,
            'close': exit,
            'exit': exit,
            '.': exit,
            'костиль':wrong_command
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
from decorator import input_error
from functions import parser_string, wrong_command
from classes import contacts

"""В ході роботи над дз я щось поламав і тепер програма не вивалюється 
з циклу при отриманні команди exit . Хоча 17 рядок цього файлу (print("Good bye!"))
відтворюється. У блок finally(рядки 23-24) теж потрапляє"""


@input_error
def main():
    try:
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
    finally:
        contacts.save_contacts_to_file()


if __name__ == '__main__':
    contacts.load_contacts_from_file()
    main()

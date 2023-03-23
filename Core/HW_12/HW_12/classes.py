from decorator import input_error
from collections import UserDict
import datetime
import pickle


class AdressBook(UserDict):

    @input_error
    def add_record(self, record):
        self[record.name.value] = record

    def iterator(self, count=5):
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

    def get_allthe_data(self):
        return self.data

    @input_error
    def search(self, value):
        result = []
        value = str(value[0])
        for i in self.get_allthe_data().values():
            if str(value) in str(i.name.value):
                result.append(i)
                continue
            for j in i.phone:
                if value in j.value:
                    result.append(i)
        if not result:
            raise ValueError('contacts not found')
        return result

    def save_contacts_to_file(self):
        with open('contacts.pickle', 'wb') as f:
            pickle.dump(self, f)
            # print('saved')

    def load_contacts_from_file(self):
        try:
            with open('contacts.pickle', 'rb') as f:
                self.data = pickle.load(f)
                # print('loaded')
        except FileNotFoundError:
            pass


class Record():
    def __init__(self, name, phone=[], birthday=None):
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
        # print(birthday)
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
    def __init__(self, phone=None):
        self.__value = None
        self.value = phone

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, phone):
        if phone.isnumeric():
            self.__value = phone
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
        # if  self.__value==re.fullmatch('\d{2}[.]\d{2}[.]\d{4}',birthday):
        # self.__value = birthday
        now = datetime.datetime.now()
        birth_day = datetime.datetime.strptime(birthday, '%d.%m.%Y').date()
        if birth_day > now.date():
            raise ValueError('birthdate must be less then the date today')
        else:
            self.__value = birthday


contacts = AdressBook()

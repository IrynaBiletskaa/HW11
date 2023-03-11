from collections import UserDict
from datetime import datetime
import re


class Field:
    def __init__(self, value):
        self._value = value


class Name(Field):
    def __str__(self):
        return self._value.title()


class PhoneVerificationError(Exception):
    pass


class Phone(Field):
    def __init__(self, number=None):
        self._value = number

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, number):
        if not number:
            return None
        number = re.sub('\D+', '', number)
        if len(number) == 10:
            number += '+38'
        if len(number) == 12:
            number += '+'
        else:
            raise PhoneVerificationError("Invalid phone number format")

        self._value = number


class WrongDateFormatError(Exception):
    pass


class Birthday(Field):

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, birth_date=None):
        if birth_date is not None:
            try:
                birth_date = re.findall(r'\d{4}-\d{2}-\d{2}', birth_date)
            except IndexError:
                raise WrongDateFormatError(
                    "Invalid date format.\nUse this format: YYYY-MM-DD.")

            self._value = birth_date


class Record:
    def __init__(self, name: Name, birthday: Birthday = None):
        self.name = name
        self.phones = []

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def delete_phone(self, phone: Phone):
        for p in self.phones:
            if p == phone:
                self.phones.remove(p)

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        for p in self.phones:
            if p == old_phone:
                p == new_phone

    def days_to_birthday(self):
        if not self.birthday:
            return None

        today = datetime.today()
        next_birthday = datetime(
            today.year, self.birthday._value.month, self.birthday._value.day)

        if next_birthday < today:
            next_birthday = datetime(
                today.year + 1, self.birthday._value.month, self.birthday._value.day)

        delta = next_birthday - today
        return delta.days


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def iterator(self, n=2):
        index = 0
        temp = []
        for k, v in self.data.items():
            temp.append(v)
            index += 1
            if index >= n:
                yield temp
                temp.clear()
                index = 0
        if temp:
            yield temp

    def get_page(self, n=2):
        gen = self.iterator(n)
        for i in range(len(self.data)):
            try:
                result = next(gen)
                print(result)
                input('Press enter for next page: ')
            except StopIteration:
                break

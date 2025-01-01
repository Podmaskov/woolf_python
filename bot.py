from collections import UserDict
from datetime import datetime, timedelta
import re

# ======================= Класи для Адресної Книги =======================

class Field:
    """
    Базовий клас для полів запису.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """
    Клас для зберігання імені контакту.
    Обов'язкове поле.
    """
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)


class Phone(Field):
    """
    Клас для зберігання номера телефону.
    Має валідацію формату (10 цифр).
    """
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

    @staticmethod
    def validate_phone(phone):
        """
        Валідує номер телефону.
        Потрібно мати саме 10 цифр.
        """
        pattern = r'^\d{10}$'
        return re.match(pattern, phone) is not None


class Birthday(Field):
    """
    Клас для зберігання дня народження.
    Необов'язкове поле, але може бути тільки одне.
    """
    def __init__(self, value):
        try:
            # Перетворення рядка на об'єкт datetime
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

    def __str__(self):
        return self.value


class Record:
    """
    Клас для зберігання інформації про контакт,
    включаючи ім'я, список телефонів та день народження.
    """
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        """
        Додає новий телефон до списку.
        """
        phone_obj = Phone(phone)
        if phone_obj.value not in [p.value for p in self.phones]:
            self.phones.append(phone_obj)
            return "Phone added."
        else:
            return "Phone already exists."

    def remove_phone(self, phone):
        """
        Видаляє телефон з списку.
        """
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return "Phone removed."
        raise KeyError

    def edit_phone(self, old_phone, new_phone):
        """
        Редагує існуючий телефон.
        """
        for p in self.phones:
            if p.value == old_phone:
                p.value = Phone(new_phone).value  # Валідація нового телефону
                return "Phone updated."
        raise KeyError

    def find_phone(self, phone):
        """
        Повертає телефон, якщо він існує.
        """
        for p in self.phones:
            if p.value == phone:
                return p.value
        raise KeyError

    def get_phones(self):
        """
        Повертає всі телефони у форматі рядка.
        """
        return "; ".join(p.value for p in self.phones)

    def add_birthday(self, birthday):
        """
        Додає день народження до контакту.
        """
        if self.birthday is not None:
            return "Birthday already exists."
        self.birthday = Birthday(birthday)
        return "Birthday added."

    def show_birthday(self):
        """
        Показує день народження контакту.
        """
        if self.birthday:
            return f"Birthday: {self.birthday.value}"
        return "No birthday set."

    def days_to_birthday(self):
        """
        Обчислює кількість днів до наступного дня народження.
        """
        today = datetime.today().date()
        birthday_date = datetime.strptime(self.birthday.value, "%d.%m.%Y").date()
        birthday_this_year = birthday_date.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        delta = birthday_this_year - today
        return delta.days

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones) if self.phones else "No phones"
        birthday = self.birthday.value if self.birthday else "No birthday"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}"


class AddressBook(UserDict):
    """
    Клас для зберігання та управління записами контактів.
    """
    def add_record(self, record):
        """
        Додає запис до AddressBook.
        """
        self.data[record.name.value] = record

    def find(self, name):
        """
        Знаходить запис за ім'ям.
        """
        return self.data.get(name)

    def delete(self, name):
        """
        Видаляє запис за ім'ям.
        """
        if name in self.data:
            del self.data[name]
            return "Contact deleted."
        else:
            raise KeyError

    def get_upcoming_birthdays(self):
        """
        Повертає список записів, у яких день народження на наступний тиждень.
        """
        upcoming = []
        today = datetime.today().date()
        for record in self.data.values():
            if record.birthday:
                days = record.days_to_birthday()
                if 0 <= days <= 7:
                    upcoming.append({
                        "name": record.name.value,
                        "congratulation_date": (today + timedelta(days=days)).strftime("%d.%m.%Y")
                    })
        return upcoming

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

# ======================= Декоратори та Функції Бота =======================

def input_error(func):
    """
    Декоратор для обробки помилок введення користувача.
    Обробляє ValueError, KeyError, IndexError.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            return str(ve)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter the argument for the command."
    return inner


def parse_input(user_input):
    """
    Парсить введене користувачем введення.
    Повертає команду та список аргументів.
    """
    parts = user_input.strip().split()
    cmd = parts[0].lower() if parts else ""
    args = parts[1:]
    return cmd, args


@input_error
def add_contact(args, book: AddressBook):
    """
    Додає контакт до AddressBook.
    Викликає метод Record.add_phone для додавання телефону.
    """
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")
    name = args[0]
    phone = args[1]
    record = book.find(name)
    message = "Contact added."
    if record is None:
        record = Record(name)
        book.add_record(record)
    else:
        message = "Contact updated."
    result = record.add_phone(phone)
    return f"{message} {result}"


@input_error
def change_contact(args, book: AddressBook):
    """
    Змінює телефон існуючого контакту.
    """
    if len(args) != 3:
        raise ValueError("Change command requires name, old_phone, new_phone.")
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        return record.edit_phone(old_phone, new_phone)
    else:
        raise KeyError


@input_error
def get_phone(args, book: AddressBook):
    """
    Повертає телефони контакту за іменем.
    """
    if len(args) != 1:
        raise ValueError("Give me the contact name.")
    name = args[0]
    record = book.find(name)
    if record:
        return record.get_phones()
    else:
        raise KeyError


@input_error
def add_birthday(args, book: AddressBook):
    """
    Додає день народження до контакту.
    """
    if len(args) != 2:
        raise ValueError("Add_birthday command requires name and birthday.")
    name, birthday = args
    record = book.find(name)
    if record:
        return record.add_birthday(birthday)
    else:
        raise KeyError


@input_error
def show_birthday(args, book: AddressBook):
    """
    Показує день народження контакту за іменем.
    """
    if len(args) != 1:
        raise ValueError("Show_birthday command requires contact name.")
    name = args[0]
    record = book.find(name)
    if record:
        return record.show_birthday()
    else:
        raise KeyError


@input_error
def birthdays(args, book: AddressBook):
    """
    Повертає список контактів з дніми народженнями на наступний тиждень.
    """
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays in the next week."
    return "\n".join(f"{item['name']} - {item['congratulation_date']}" for item in upcoming)


def list_contacts(book: AddressBook):
    """
    Повертає всі контакти в AddressBook.
    """
    if not book.data:
        return "No contacts found."
    return "\n".join(str(record) for record in book.data.values())


def main():
    """
    Головна функція бота.
    """
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        if not user_input.strip():
            print("Enter a command.")
            continue
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(get_phone(args, book))
        elif command == "all":
            print(list_contacts(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
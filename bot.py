from collections import UserDict
import re

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter the argument for the command."
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

@input_error
def add_contact(args, contacts):
    if len(args) != 2:
        raise ValueError
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    if len(args) != 2:
        raise ValueError
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact updated."
    else:
        raise KeyError

@input_error
def get_phone(args, contacts):
    if len(args) != 1:
        raise ValueError
    name = args[0]
    if name in contacts:
        return f"{name}: {contacts[name]}"
    else:
        raise KeyError

def list_contacts(contacts):
    if not contacts:
        return "No contacts found."
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())

def main():
    contacts = {}
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
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(get_phone(args, contacts))
        elif command == "all":
            print(list_contacts(contacts))
        else:
            print("Invalid command.")

# if __name__ == "__main__":
#     main()

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

class Record:
    """
    Клас для зберігання інформації про контакт,
    включаючи ім'я та список телефонів.
    """
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

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

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {self.get_phones()}"

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

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def add_contact(args, contacts):
    if len(args) != 2 or not args[0] or not args[1]:
        return "Error: Command 'add' requires exactly 2 non-empty arguments."
    name, phone = args
    contacts[name] = phone
    return "Contact added."

def change_contact(args, contacts):
    if len(args) != 2 or not args[0] or not args[1]:
        return "Error: Command 'change' requires exactly 2 non-empty arguments."
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact updated."
    else:
        return "Error: Contact not found."

def get_phone(args, contacts):
    if len(args) != 1 or not args[0]:
        return "Error: Command 'phone' requires exactly 1 non-empty argument."
    name = args[0]
    if name in contacts:
        return f"{name}: {contacts[name]}"
    else:
        return "Error: Contact not found."

def list_contacts(contacts):
    if not contacts:
        return "No contacts found."
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())

def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
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

if __name__ == "__main__":
    main()
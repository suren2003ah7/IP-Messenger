import json

from contact import Contact

PORT = 5050

contacts: list[Contact] = []

def print_help():
    print("")
    print("-------------------------------------------------------------------------------------------------------------------------------------------")
    print("Available commands:")
    print("  add <contact_name> <ipv4> <ipv6>                       - Add a new contact, place _ if any of the IP's is not known")
    print("  contacts                                               - List all saved contacts")
    print("  configure <ipv6> <scope_id>                            - Configure your IPv6 and its scope id in order to send messages through IPv6")
    print("  delete <contact_name>                                  - Delete a contact by name")
    print("  delete -all                                            - Delete all contacts")
    print("  edit <contact_name> [-name NEW] [-ip NEW] [-ipv6 NEW]  - Edit a contact's name and/or IP addresses")
    print("  export <filename>                                      - Export contacts to a JSON file")
    print("  help                                                   - Show this help message")
    print("  import <filename>                                      - Import contacts from a JSON file")
    print("  ip                                                     - Show your current LAN IP address")
    print("  ipv6                                                   - Show the manually configured IPv6 address")
    print("  q                                                      - Quit the application")
    print("  send <contact_name> <message>                          - Send a message to the contact by name")
    print("-------------------------------------------------------------------------------------------------------------------------------------------")
    print("")

def print_contacts():
    if len(contacts) == 0:
        print("You have no contacts!")
        return
    i = 1
    for contact in contacts:
        print(str(i) + ") " + str(contact))
        i+=1

def add_contact(name, ip, ipv6):
    for contact in contacts:
        if contact.name == name:
            print(f"Unable to create contact as the name {name} is already in use!")
            return
        
    if ip == "_" and ipv6 == "_":
        print("At least one IP address must be present!")
        return

    contacts.append(Contact(name, ip, ipv6))
    print("Contact successfully added!")

def delete_contact_by_name(name):
    for contact in contacts:
        if contact.name == name:
            contacts.remove(contact)
            print("Contact removed!")
            return
    print("Contact not found!")

def delete_all_contacts():
    contacts.clear()
    print("Deleted all contacts!")

def edit_contact_by_name(name, new_name, new_ip, new_ipv6):
    for contact in contacts:
        if contact.name == new_name:
            print(f"The name {new_name} is already in use!")
            return

    for contact in contacts:
        if contact.name == name:
            if new_name != "":
                contact.name = new_name
            if new_ip != "":
                contact.ip = new_ip
            if new_ipv6 != "":
                contact.ipv6 = new_ipv6
            print("Contact modified to: " + str(contact))
            return
    print("Contact not found!")

def import_from_json(filename):
    with open(filename, "r") as file:
        imported_contacts = json.load(file)

    for contact in imported_contacts:
        add_contact(contact["name"], contact["ip"], contact["ipv6"])
    
    print(f"Successfully imported from {filename}")

def export_to_json(filename):
    with open(filename, "w") as file:
        list_of_dictionaries = []
        for contact in contacts:
            list_of_dictionaries.append(contact.to_dictionary_form())
        json.dump(list_of_dictionaries, file, indent=2)
    
    print(f"Successfully exported to {filename}")
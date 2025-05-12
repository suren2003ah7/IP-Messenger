import client_utils as cutl
import threading

import sender
from receiver import stop_event, listen_ipv4, listen_ipv6

print("")
print("--------------------------------------------------------------------------------------------------------------")
print("Hello and welcome to IP Messanger! Message freely with your friends and family using their IP addresses!")
print("To view the list of valid commands type \"help\"")
print("To exit type \"q\"")
print("--------------------------------------------------------------------------------------------------------------")
print("")

receiver = threading.Thread(target=listen_ipv4)
receiver.start()

receiveripv6 = threading.Thread(target=listen_ipv6)
receiveripv6.start()

while True:
    user_input = input("> ")
    
    if user_input == "q":
        break
    elif user_input == "help":
        cutl.print_help()
    elif user_input == "contacts":
        cutl.print_contacts()
    elif user_input[0:3] == "add":
        information = user_input.split(" ")
        if len(information) != 4:
            print("Inappropriate usage of command \"add\"")
            continue
        cutl.add_contact(information[1], information[2], information[3])
    elif user_input[0:6] == "delete":
        information = user_input.split(" ")
        if len(information) != 2:
            print("Inappropriate usage of command \"delete\"")
            continue
        if information[1] == "-all":
            cutl.delete_all_contacts()
            continue
        cutl.delete_contact_by_name(information[1])
    elif user_input[0:4] == "edit":
        information = user_input.split(" ")
        if len(information) < 2:
            print("Inappropriate usage of command \"edit\"")
            continue
        name = information[1]
        newname = ""
        newip = ""
        newipv6 = ""
        if "-name" in information:
            newname = information[information.index("-name") + 1]
        if "-ip" in information:
            newip = information[information.index("-ip") + 1]
        if "-ipv6" in information:
            newipv6 = information[information.index("-ipv6") + 1]
        cutl.edit_contact_by_name(name, newname, newip, newipv6)
    elif user_input[0:6] == "import":
        information = user_input.split(" ")
        if len(information) != 2:
            print("Inappropriate usage of command \"import\"")
            continue
        cutl.import_from_json(information[1])
    elif user_input[0:6] == "export":
        information = user_input.split(" ")
        if len(information) != 2:
            print("Inappropriate usage of command \"export\"")
            continue
        cutl.export_to_json(information[1])
    elif user_input[0:4] == "send":
        name = user_input.split(" ")[1]
        index = 6 + len(name)
        sender.send_message(name, user_input[index:])
    elif user_input == "ip":
        print(f"Your IPv4 is: {sender.get_my_ip()}")
    elif user_input[0:9] == "configure":
        sender.set_ipv6(user_input.split(" ")[1])
    elif user_input == "ipv6":
        print(f"Your IPv6 is: {sender.MY_IPv6}")
    else:
        print("Invalid command!")

print("Terminating...")
stop_event.set()
receiver.join()
receiveripv6.join()
print("Thank you for using IP Messanger! Have a nice day!")
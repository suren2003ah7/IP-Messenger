import client_utils as cutl
import threading

from sender import send_message, get_my_ip
from receiver import listen_to_messages, stop_event

print("")
print("--------------------------------------------------------------------------------------------------------------")
print("Hello and welcome to IP Messanger! Message freely with your friends and family using their IP addresses!")
print("To view the list of valid commands type \"help\"")
print("To exit type \"q\"")
print("--------------------------------------------------------------------------------------------------------------")
print("")

receiver = threading.Thread(target=listen_to_messages)
receiver.start()

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
        if len(information) != 3:
            print("Inappropriate usage of command \"add\"")
            continue
        cutl.add_contact(information[1], information[2])
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
        if "-name" in information:
            newname = information[information.index("-name") + 1]
        if "-ip" in information:
            newip = information[information.index("-ip") + 1]
        cutl.edit_contact_by_name(name, newname, newip)
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
        send_message(name, user_input[index:])
    elif user_input == "ip":
        print(f"Your IP is: {get_my_ip()}")
    else:
        print("Invalid command!")

print("Terminating...")
stop_event.set()
receiver.join()
print("Thank you for using IP Messanger! Have a nice day!")
import xml.etree.ElementTree as ET
import socket as sock
import threading

from client_utils import contacts, PORT

BUFFER_SIZE = 1024
NAMESPACE = {"jc": "jabber:client"}

stop_event = threading.Event()

def handle_client(contact_client, address):
    try:
        data = contact_client.recv(BUFFER_SIZE)
        decoded_data = data.decode()
        xmpp_message = ET.fromstring(decoded_data)

        sender_ip = xmpp_message.attrib.get("from")
        message = xmpp_message.find("jc:body", NAMESPACE).text

        display_name = sender_ip
        for contact in contacts:
            if contact.ip == sender_ip or contact.ip6 == sender_ip:
                display_name = contact.name

        print("")
        print(f"[Message from {display_name}]: {message}")
        print("> ", end="", flush=True)
    finally:
        contact_client.close()

def listen_ipv4():
    s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    s.bind(("0.0.0.0", PORT))
    s.listen(5)
    s.settimeout(1.0)

    while not stop_event.is_set():
        try:
            contact_client, address = s.accept()
            threading.Thread(target=handle_client, args=(contact_client, address)).start()
        except sock.timeout:
            continue
        except OSError:
            break

    s.close()

def listen_ipv6():
    s = sock.socket(sock.AF_INET6, sock.SOCK_STREAM)
    s.bind(("::", PORT))
    s.listen(5)
    s.settimeout(1.0)

    while not stop_event.is_set():
        try:
            contact_client, address = s.accept()
            threading.Thread(target=handle_client, args=(contact_client, address)).start()
        except sock.timeout:
            continue
        except OSError:
            break

    s.close()
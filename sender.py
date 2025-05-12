import xml.etree.ElementTree as ET
import socket as sock
import subprocess
import re

from client_utils import contacts, PORT

MY_IPv6 = "_"

def set_ipv6(new_ipv6):
    global MY_IPv6
    MY_IPv6 = new_ipv6
    print(f"Your IPv6 is configured to: {MY_IPv6}")

def get_my_ip():
    try:
        result = subprocess.run(["ifconfig"], capture_output=True, text=True, check=True)
        output = result.stdout

        match = re.search(r"inet ((?:192|10|172\.(?:1[6-9]|2[0-9]|3[0-1]))\.\d+\.\d+\.\d+)", output)
        if match:
            return match.group(1)
    except Exception:
        pass

    try:
        result = subprocess.run(["ipconfig"], capture_output=True, text=True, check=True)
        output = result.stdout

        match = re.search(r"IPv4 Address[^\d]*: ((?:192|10|172\.(?:1[6-9]|2[0-9]|3[0-1]))\.\d+\.\d+\.\d+)", output)
        if match:
            return match.group(1)
    except Exception:
        pass

    print("Unable to identify local IP address!")
    return None

def message_to_xml_string(to_ip, message):
    attributes = {
        "to": to_ip,
        "from": get_my_ip(),
        "type": "chat",
        "xmlns": "jabber:client"
    }

    xmpp_message = ET.Element("message", attributes)
    ET.SubElement(xmpp_message, "body").text = message

    return ET.tostring(xmpp_message, encoding="unicode")

def message_to_xml_string_ipv6(to_ip, message):
    attributes = {
        "to": to_ip,
        "from": MY_IPv6,
        "type": "chat",
        "xmlns": "jabber:client"
    }

    xmpp_message = ET.Element("message", attributes)
    ET.SubElement(xmpp_message, "body").text = message

    return ET.tostring(xmpp_message, encoding="unicode")

def send_message(name, message):
    ip = "_"
    ipv6 = "_"
    for contact in contacts:
        if contact.name == name:
            ip = contact.ip
            ipv6 = contact.ipv6
            break
    
    if ip == "_" and ipv6 == "_":
        print("Contact not found!")
        return
    
    if ip != "_":
        xmpp_message = message_to_xml_string(ip, message)

        with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
            try:
                s.connect((ip, PORT))
                s.sendall(xmpp_message.encode())
            except ConnectionRefusedError:
                print(f"Unable to establish connection with user! IPv4: {ip}")
                s.close()
    else:
        if MY_IPv6 == "_":
            print("Configure your IPv6 first!")
            return

        xmpp_message = message_to_xml_string_ipv6(ipv6, message)

        with sock.socket(sock.AF_INET6, sock.SOCK_STREAM) as s:
            try:
                s.connect((ipv6, PORT, 0, 0))
                s.sendall(xmpp_message.encode())
            except ConnectionRefusedError:
                print(f"Unable to establish connection with user! IPv6: {ipv6}")
                s.close()


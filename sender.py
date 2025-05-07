import xml.etree.ElementTree as ET
import socket as sock
import subprocess
import re

from client_utils import contacts, PORT

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

def send_message(name, message):
    ip = ""
    for contact in contacts:
        if contact.name == name:
            ip = contact.ip
            break
    
    if ip == "":
        print("Contact not found!")
        return
    
    xmpp_message = message_to_xml_string(ip, message)

    with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
        try:
            s.connect((ip, PORT))
            s.sendall(xmpp_message.encode())
        except ConnectionRefusedError:
            print(f"Unable to establish connection with user! IP: {ip}")
            s.close()


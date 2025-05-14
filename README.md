# IP Messenger CLI

A lightweight command-line IP messenger that allows direct messaging between clients over local IPv4 and IPv6.

## Features

* Add, list, edit, and delete contacts
* Support for IPv4 (auto-detected via `ifconfig`) and IPv6 (manual configuration with scope ID)
* Export and import contacts to/from JSON
* Show current LAN IPv4 and configured IPv6 addresses
* Send messages directly to contacts by name

## Prerequisites

* Python 3.13
* Standard library modules (no external dependencies)
* `ifconfig` available for automatic IPv4 detection (may detect incorrectly)

## Installation and Running

1. Download the ZIP from the GitHub repository and unzip.

### Linux/Unix

```bash
make
```

### Windows

```powershell
python3 client.py client_utils.py contact.py sender.py receiver.py
```

## Usage

At the application prompt, use the following commands:

| Command                                                 | Description                              |
| ------------------------------------------------------- | ---------------------------------------- |
| `add <contact_name> <ipv4> <ipv6>`                      | Add a new contact (`_` if IP unknown)    |
| `contacts`                                              | List all saved contacts                  |
| `configure <ipv6> <scope_id>`                           | Configure your IPv6 address and scope ID |
| `delete <contact_name>`                                 | Delete a contact by name                 |
| `delete -all`                                           | Delete all contacts                      |
| `edit <contact_name> [-name NEW] [-ip NEW] [-ipv6 NEW]` | Edit a contact's name or IP addresses    |
| `export <filename>`                                     | Export contacts to a JSON file           |
| `import <filename>`                                     | Import contacts from a JSON file         |
| `ip`                                                    | Show your current LAN IPv4 address       |
| `ipv6`                                                  | Show your configured IPv6 address        |
| `send <contact_name> <message>`                         | Send a message to the contact            |
| `help`                                                  | Show this help message                   |
| `q`                                                     | Quit the application                     |

## Example

```bash
> add Alice 192.168.1.5 fe80::1ff:fe23:4567:890a
> send Alice Hello, Alice!
```

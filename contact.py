class Contact:
    def __init__(self, name, ip, ipv6):
        self.name = name
        self.ip = ip
        self.ipv6 = ipv6
    
    def __str__(self):
        return f"Name: {self.name}, IPv4: {self.ip}, IPv6: {self.ipv6}"
    
    def to_dictionary_form(self):
        return {
            "name": self.name,
            "ip": self.ip,
            "ipv6": self.ipv6
        }
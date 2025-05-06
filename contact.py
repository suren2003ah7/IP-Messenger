class Contact:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
    
    def __str__(self):
        return f"Name: {self.name}, IP: {self.ip}"
    
    def to_dictionary_form(self):
        return {
            "name": self.name,
            "ip": self.ip
        }
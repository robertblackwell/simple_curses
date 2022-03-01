import ipaddress

class Text:
    def __init__(self):
        pass

    def validate(self, str):
        try:
            return str
        except ValueError:
            return None

    def error_message(self):
        return "Invalid text string"

class Integer:
    def __init__(self):
        pass

    def validate(self, str):
        try:
            i = int(str)
            return i
        except ValueError:
            return None

    def error_message(self):
        return "Invalid integer"

class Float:
    def __init__(self):
        pass

    def validate(self, str):
        try:
            f = float(str)
            return f
        except ValueError:
            return None

    def error_message(self):
        return "Invalid floating point number"

class IPAddress:
    def __init__(self):
        pass

    def validate(self, str):
        try:
            i = ipaddress.ip_address(str)
            return i
        except ValueError:
            return None

    def error_message(self):
        return "Invalid ip address"

class IPNetwork:
    def __init__(self):
        pass

    def validate(self, str):
        try:
            i = ipaddress.ip_network(str)
            return i
        except ValueError:
            return None

    def error_message(self):
        return "Invalid ip network"

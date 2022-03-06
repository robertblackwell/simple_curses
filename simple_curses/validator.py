import ipaddress
from typing import TypeVar, List

T = TypeVar("T")

class ArrayOf:
    def __init__(self, validator:T):
        self.validator = validator
    
    def validate(self, ar:List[str]):
        result = []
        for s in ar:
            try:
                r = self.validator.validate(s)
                result.append(r)
            except ValueError:
                return None
        return result
    def error_message(self):
        return "Invalid text string for array of {}".format(self.validator.error_message())

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

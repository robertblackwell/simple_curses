import time
import ipaddress
import string
import re
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

class TimeOfDay24:
    def __init__(self):
        pass
    def validate(self, astr):
        try:
            i = time.strptime(astr, "%H:%M")
            return i
        except ValueError:
            return None

    def error_message(self):
        return "Invalid ip 24hr time of day - correct format is HH:MM "


def time12_to_24(time_string):
    time12 = time_string.strip().lower()
    is_am = "am" in time12
    is_pm = "pm" in time12
    if not (is_am or is_pm):
        return None
    time_list = list(map(int, time12[:-2].strip().split(':')))            
    if not len(time_list) == 2:
        return None
    if not 0 <= time_list[0] <= 12:
        return None
    if not 0 <= time_list[1] <= 59:
        return None
    if not is_pm and time_list[0] == 12:
        time_list[0] = 0
    if is_pm and time_list[0] < 12:
        time_list[0] += 12

    return (':'.join(map(lambda x: str(x).rjust(2, '0'), time_list)))
class TimeOfDay12:
    def __init__(self):
        pass
    def validate(self, astr: str):
        try:
            intermediate = time12_to_24(astr)
            if not intermediate:
                raise ValueError("conversion 12 H time to 24H time failed")
            i = time.strptime(intermediate, "%H:%M")
            return i
        except ValueError:
            return None

    def error_message(self):
        return "Invalid 12hr time of day - correct format is HH:MM AM or HH:MM PM"

import time
import ipaddress
from typing import TypeVar, List, Union, Generic, Any, Dict, Optional, Any
import pathlib

T = TypeVar('T')


class ResultType(Generic[T]):
    def __init__(self, value: Union[T, None], err_msg: str = ""):
        self.value: Union[T, None] = value
        self.ok: bool = value is not None
        self.err_msg: str = err_msg

    def is_ok(self) -> bool:
        return self.ok and self.value is not None

    def get_value(self) -> Optional[T]:
        if not self.is_ok():
            raise RuntimeError("cannot get_value of ResultType with ok==False")
        else:
            return self.value

    def get_errmsg(self):
        if self.is_ok():
            raise RuntimeError("cannot get_errmsgof ResultType with ok==True")
        else:
            return self.err_msg

class Text:
    def __init__(self):
        pass

    def validate(self, astr):
        try:
            return astr
        except ValueError:
            return None

    def error_message(self):
        return "Invalid text string"

def validate_text(astr):
    return Text().validate(astr)

class Integer:
    def __init__(self):
        pass

    def validate(self, astr):
        try:
            i = int(astr)
            return i
        except ValueError:
            return None

    def error_message(self):
        return "Invalid integer"


class Float:
    def __init__(self):
        pass

    def validate(self, astr):
        try:
            f = float(astr)
            return f
        except ValueError:
            return None

    def error_message(self):
        return "Invalid floating point number"


class IPAddress:
    def __init__(self):
        pass

    def validate(self, astr):
        try:
            i = ipaddress.ip_address(astr)
            return i
        except ValueError:
            return None

    def error_message(self):
        return "Invalid ip address"


class IPNetwork:
    def __init__(self):
        pass

    def validate(self, astr):
        try:
            i = ipaddress.ip_network(astr)
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
        return "Invalid 24hr time of day - correct format is HH:MM "


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


class Path:
    def __init__(self):
        self.astr = None

    def validate(self, astr: str):
        self.astr = astr
        try:
            p = pathlib.Path(astr)
            return p
        except ValueError:
            return None

    def error_message(self):
        return "Invalid file path {}".format(self.astr)


class PathExists:
    def __init__(self):
        self.astr = None
        pass

    def validate(self, astr: str):
        self.astr = astr
        try:
            p = pathlib.Path(astr)
            if not p.exists():
                raise ValueError()
            return p
        except ValueError:
            return None

    def error_message(self):
        return "File path {} is either invalid or does not exists".format(self.astr)

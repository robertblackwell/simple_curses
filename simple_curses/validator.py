import time
import ipaddress
from typing import TypeVar, List, Union, Generic, Any, Dict, Optional
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


class WidgetSingleValue:
    def __init__(self, str_value: str, parsed_value: Union[Any, None], ok: bool, err_msg=""):
        self.type = "WidgetSingleValue"
        self.parsed_value = parsed_value
        self.str_value = str_value
        self.err_msg = err_msg

    def is_ok(self):
        return self.parsed_value is not None

    def get_string_value(self) -> str:
        return self.str_value

    def get_parsed_value(self) -> Any:
        if self.is_ok():
            return self.parsed_value
        raise ValueError("WidgetSingleValue does not have parsed value")


class WidgetListOfValues:
    def __init__(self):
        self.values = []
        self.ok = True
        self.type = "WidgetListOfValues"

    def xappend(self, str_value: str, parsed_value: Union[Any, None], ok: bool):
        self.values.append(WidgetSingleValue(str_value, parsed_value, ok))
        self.ok = self.ok and ok

    def append(self, wsv: WidgetSingleValue):
        self.values.append(wsv)
        self.ok = self.ok and wsv.is_ok()

    def is_ok(self):
        return self.ok

    def get_string_values(self):
        v = []
        for tmp in self.values:
            v.append(tmp.get_string_value())
        return v

    def get_string_value(self):
        return self.get_string_values()

    def get_parsed_values(self):
        v = []
        for tmp in self.values:
            v.append(tmp.get_parsed_value())
        return v

    def get_parsed_value(self):
        return self.get_parsed_values()


class XXWidgetSingleValue:
    def __init__(self, str_value: str, parsed_value: Union[Any, None], ok: bool, err_msg=''):
        self.parsed_value = parsed_value
        self.str_value = str_value
        self.ok = ok
        self.error_messages = err_msg


class XXWidgetListOfValues:
    def __init__(self):
        self.values = []
        self.ok = True

    def append(self, single_value: WidgetSingleValue):
        self.values.append(single_value)
        self.ok = self.ok and single_value.is_ok()


WidgetValue = Union[WidgetSingleValue, WidgetListOfValues]
ViewValueType = ResultType[Dict[str, WidgetValue]]


class ViewValues:
    def __init__(self):
        self.ok = True

    def is_ok(self):
        return self.ok

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value: WidgetValue):
        setattr(self, key, value)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def value_keys(self):
        """
        Return the keys associated with widget values in this instance of a ViewValues class.
        Returns a list of keys such that ViewValues[k] will return a WidgetValue
        """
        keys = []
        for k in self.__dict__.keys():
            if k != "ok":
                keys.append(k)
        return keys

    def string_value_dict(self):
        v = {}
        d = self.__dict__
        for k in self.__dict__.keys():
            if k != "ok":
                wv: WidgetValue = self[k]
                v[k] = wv.get_string_value()
        return v

    def parsed_value_dict(self):
        v = {}
        for k in self.__dict__.keys():
            if k != "ok":
                wv: WidgetValue = self[k]
                v[k] = wv.get_parsed_value()
        return v

    def invalid_values_dict(self):
        v = {}
        for k in self.__dict__.keys():
            if k != "ok":
                wv: WidgetValue = self[k]
                if not wv.is_ok():
                    v[k] = wv.get_string_value()
        return v


class ArrayOf:
    def __init__(self, validator):
        self.validator = validator

    def validate(self, ar: List[str]):
        ok = True
        result = WidgetListOfValues()
        for s in ar:
            try:
                r: WidgetValue = self.validator.validate(s)
                ok = ok and r.is_ok()
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
            return WidgetSingleValue(str, str, True)
        except ValueError:
            return WidgetSingleValue(str, None, False, "INvalid Text String")

    def error_message(self):
        return "Invalid text string"


class Integer:
    def __init__(self):
        pass

    def validate(self, astr):
        try:
            i = int(astr)
            return WidgetSingleValue(astr, i, True)
        except ValueError:
            return WidgetSingleValue(astr, None, False, "Invalid Integer")

    def error_message(self):
        return "Invalid integer"


class Float:
    def __init__(self):
        pass

    def validate(self, astr):
        try:
            f = float(astr)
            return WidgetSingleValue(f, astr, True)
        except ValueError:
            return WidgetSingleValue(astr, None, False, "Invalid Floating point number")

    def error_message(self):
        return "Invalid floating point number"


class IPAddress:
    def __init__(self):
        pass

    def validate(self, astr):
        try:
            i = ipaddress.ip_address(astr)
            return WidgetSingleValue(astr, i, True)
        except ValueError:
            return WidgetSingleValue(astr, None, False, "Invalid IP address")

    def error_message(self):
        return "Invalid ip address"


class IPNetwork:
    def __init__(self):
        pass

    def validate(self, astr):
        try:
            i = ipaddress.ip_network(astr)
            return WidgetSingleValue(astr, i, True)
        except ValueError:
            return WidgetSingleValue(astr, None, False, "Invalid IP address")

    def error_message(self):
        return "Invalid ip network"


class TimeOfDay24:
    def __init__(self):
        pass

    def validate(self, astr):
        try:
            i = time.strptime(astr, "%H:%M")
            return WidgetSingleValue(astr, i, True)
        except ValueError:
            return WidgetSingleValue(astr, None, False, "Invalid 24hr time of day - correct format is HH:MM ")

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
            return WidgetSingleValue(astr, i, True)
        except ValueError:
            return WidgetSingleValue(astr, None, False,
                                     "Invalid 12hr time of day - correct format is HH:MM AM or HH:MM PM")

    def error_message(self):
        return "Invalid 12hr time of day - correct format is HH:MM AM or HH:MM PM"


class Path:
    def __init__(self):
        self.astr = None

    def validate(self, astr: str):
        self.astr = astr
        try:
            p = pathlib.Path(astr)
            return WidgetSingleValue(astr, p, True)
        except ValueError:
            return WidgetSingleValue(astr, None, False, "Invalid file path {}".format(self.astr))

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
            return WidgetSingleValue(astr, p, True)
        except ValueError:
            return WidgetSingleValue(astr, None, False, "File path {} invalid or does not exist ".format(self.astr))

    def error_message(self):
        return "File path {} is either invalid or does not exists".format(self.astr)

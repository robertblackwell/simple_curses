import curses.textpad
from simple_curses import *
import pathlib
import ipaddress
# from utils import *
# from widget_base import EditableWidgetBase
# from string_buffer import StringBuffer
# import validator

# A basic text widget that allows the entry of printable characters.
# A model upon which to base more complicated text controls
# A TextWidget is composed of a label and an value field
class TextWidget(EditableWidgetBase):
    @classmethod
    def classmeth(cls):
        print("hello")

    def __init__(self, app, key: str, label: str, width: int, data: any): #, initial_value = ""):
        self.win = None
        self.id = key
        self.has_focus = False
        # self.row = relative_row
        # self.col = relative_col
        self.data = data
        # self.content = ""
        # self.content_position = 0
        self.label = label + ": "
        self.width = width
        self.height = 1
        self.start_row = 0
        self.start_col = 0

        # self.attributes = attributes
        self.app = app
        self.validator = validator.Text()
        tmp = width + len(self.label)
        # self.win = curses.newwin(1, width + len(self.label) + 2, row, col, )
        self.string_buffer = StringBuffer("", self.width)

        # these properties are for manaing the display of the conttent string during
        # entry and editing
        self.display_content_start = 0
        self.display_content_position = 0  # current cursor position in the content
        self.display_cursor_position = 0  # always between 0 .. width - that is always visible
        self.display_length = 0  # is width-1 if we are adding to the end of the string in which case the cursor is over the 'next' slot
        # if we are editing the string and the cursor is somewhere inside the content string then has the value width

    def set_enclosing_window(self, win: curses.window) -> None:
        self.win = win

    # def set_app(self, app) -> None:
    #     self.app = app
    # 
    def get_width(self) -> int:
        return len(self.label) + self.width + 2

    def get_height(self) -> int:
        return 1

    def clear(self):
        self.string_buffer.clear()

    # paint attributes for the content area so that it is visible to used
    def paint_content_area_background(self) -> None:
        tmp = self.width + len(self.label) - 1
        for i in range(0, tmp):
            if self.has_focus:
                self.win.addstr(0, i, "_")
            else:
                self.win.addstr(0, i, "_")

    # called by the containing app to paint/render the Widget
    def render(self) -> None:
        self.paint_content_area_background()
        self.win.addstr(0, 0, self.label, curses.A_BOLD)
        self.win.addstr(0, len(self.label), self.string_buffer.display_string)
        if self.has_focus:
            self.position_cursor()
        self.win.noutrefresh()

    # 
    # Positions the cursor to the current active position and makes sure it blinks.
    # The current active position is usually 1 space past the end of the currently input text
    # 
    def position_cursor(self) -> None:
        ch_under_cursor = self.string_buffer.display_string[self.string_buffer.cpos_buffer]
        self.win.addnstr(0, len(self.label) + self.string_buffer.cpos_buffer, ch_under_cursor, 1,
                         curses.A_REVERSE + curses.A_BLINK)
        self.win.noutrefresh()

    # 
    # called by the app instance to give this control focus
    # 
    def focus_accept(self) -> None:
        self.has_focus = True
        self.position_cursor()

    def focus_release(self) -> None:
        self.has_focus = False

    def get_key(self):
        return self.id

    def get_value(self) -> validator.WidgetSingleValue:
        str_value = self.string_buffer.content
        widget_value = self.validator.validate(str_value)
        return widget_value

    def set_value(self, value):
        if isinstance(value, validator.WidgetSingleValue):
            v:validator.WidgetSingleValue = value
            vv = v.str_value
            self.string_buffer.clear()
            self.string_buffer.add_string(vv)

        elif type(value) == str:
            self.string_buffer.clear()
            self.string_buffer.add_string(value)
            pass
        else:
            raise ValueError("value is invalid type:{} value:{}".format(type(value), value))


    # 
    # Called by inpput handling functions to signal to user that the last keysttroke was
    # invalid. Dont quite know what to do yet
    # 
    def invalid_input(self):
        pass

    # When a Widget has the focus every keystroke (with some small exceptions)
    # get passed to this function.
    # If the Widget handles the keystroke then it should return true
    # else should return false
    # 
    def handle_input(self, ch) -> bool:
        did_handle_ch = True
        if (ch <= 255) and (chr(ch) in string.printable):
            self.string_buffer.handle_character(chr(ch))
        elif is_edit_back(ch):
            self.string_buffer.handle_backspace()
        elif is_edit_del(ch):
            self.string_buffer.handle_delete()
        elif is_move_left(ch):
            self.string_buffer.handle_left()
        elif is_move_right(ch):
            self.string_buffer.handle_right()
        else:
            did_handle_ch = False

        self.position_cursor()
        return did_handle_ch


class IntegerWidget(TextWidget):
    def __init__(self, app, key, label, width, data): #, initial_value="0"):
        super().__init__(app, key, label, width, data)#, initial_value)
        self.validator = validator.Integer()

    def set_value(self, value):
        if type(value) == str or isinstance(value, validator.WidgetSingleValue):
            super().set_value(value)
        elif type(value) == int:
            super().set_value("{}".format(value))
        else:
            ValueError("value:{} of type {} is invalid".format(value, type(value)))


class FloatWidget(TextWidget):
    def __init__(self, app, key, label, width,  data): #, initial_value="0.0"):
        super().__init__(app, key, label, width,  data)#, initial_value)
        self.validator = validator.Float()

    def set_value(self, value):
        if type(value) == str or isinstance(value, validator.WidgetSingleValue):
            super().set_value(value)
        elif type(value) == float:
            super().set_value("{}".format(value))
        else:
            ValueError("value:{} of type {} is invalid".format(value, type(value)))


class IPAddressWidget(TextWidget):
    def __init__(self, app, key, label, width,  data): #, initial_value="192.168.0.1"):
        super().__init__(app, key, label, width,  data)#, initial_value)
        self.validator = validator.IPAddress()

    def set_value(self, value):
        if type(value) == str or isinstance(value, validator.WidgetSingleValue):
            super().set_value(value)
        elif isinstance(value, ipaddress.IPv4Address) or isinstance(value, ipaddress.IPv6Address):
            super().set_value("{}".format(value))
        else:
            ValueError("value:{} of type {} is invalid".format(value, type(value)))


class IPNetworkWidget(TextWidget):
    def __init__(self, app, key, label, width,  data): #, initial_value="192.168.0.1"):
        super().__init__(app, key, label, width,  data)#, initial_value)
        self.validator = validator.IPNetwork()

    def set_value(self, value):
        if type(value) == str or isinstance(value, validator.WidgetSingleValue):
            super().set_value(value)
        elif isinstance(value, ipaddress.IPv4Network ) or isinstance(value, ipaddress.IPv6Network):
            super().set_value("{}".format(value))
        else:
            ValueError("value:{} of type {} is invalid".format(value, type(value)))


class TimeOfDayWidget(TextWidget):
    def __init__(self, app, key, label, width,  data): #, initial_value="13:55"):
        super().__init__(app, key, label, width,  data)#, initial_value)
        self.validator = validator.TimeOfDay24()
    def set_value(self, value):
        if type(value) == str or isinstance(value, validator.WidgetSingleValue):
            super().set_value(value)
        elif isinstance(value, time.struct_time):
            super().set_value("{}".format(time.strf("%H:%M", value)))
        else:
            ValueError("value:{} of type {} is invalid".format(value, type(value)))


class PathWidget(TextWidget):
    def __init__(self, app, key, label, width,  data): #, initial_value="/fred"):
        super().__init__(app, key, label, width,  data)#, initial_value)
        self.validator = validator.Path()

    def set_value(self, value):
        if type(value) == str or isinstance(value, validator.WidgetSingleValue):
            super().set_value(value)
        elif isinstance(value, pathlib.PosixPath):
            super().set_value("{}".format(value))
        else:
            ValueError("value:{} of type {} is invalid".format(value, type(value)))


class PathExistsWidget(TextWidget):
    def __init__(self, app, key, label, width,  data): #, initial_value=" /home/robertblackwell"):
        super().__init__(app, key, label, width,  data)#, initial_value)
        self.validator = validator.PathExists()

    def set_value(self, value):
        if type(value) == str or isinstance(value, validator.WidgetSingleValue):
            super().set_value(value)
        elif isinstance(value, pathlib.PosixPath):
            super().set_value("{}".format(value))
        else:
            ValueError("value:{} of type {} is invalid".format(value, type(value)))

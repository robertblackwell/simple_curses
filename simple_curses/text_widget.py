import curses.textpad
import pathlib
import ipaddress
import time
from typing import Any
from simple_curses.keyboard import *
from simple_curses.widget_base import EditableWidgetBase
from simple_curses.string_buffer import StringBuffer
from simple_curses.theme import Theme

# A basic text widget that allows the entry of printable characters.
# A model upon which to base more complicated text controls
# A TextWidget is composed of a label and an value field
class TextWidget(EditableWidgetBase):
    @classmethod
    def classmeth(cls):
        print("hello")

    def __init__(self, app, key: str, label: str, width: int, data: Any): #, initial_value = ""):
        self.id = key
        self.has_focus = False
        self.data = data
        self.label = label + ": "
        self.width = width
        self.height = 1
        self.start_row = 0
        self.start_col = 0
        self.app = app
        self.string_buffer = StringBuffer("", self.width)

        # Deprecated - remove
        self.display_content_start = 0
        self.display_content_position = 0  # current cursor position in the content
        self.display_cursor_position = 0  # always between 0 .. width - that is always visible
        self.display_length = 0  # is width-1 if we are adding to the end of the string in which case the cursor is over the 'next' slot
        # Deprecated

    def set_enclosing_window(self, win) -> None:
        self.win = win

    def get_width(self) -> int:
        return len(self.label) + self.width + 2

    def get_height(self) -> int:
        return 1

    def clear(self):
        self.string_buffer.clear()

    def paint_content_area_background(self) -> None:
        """paint attributes for the content area so that it is visible to use"""
        tmp = self.width + len(self.label) - 1
        for i in range(0, tmp):
            if self.has_focus:
                self.win.addstr(0, i, "_", Theme.instance().value_attr(True))
            else:
                self.win.addstr(0, i, "_", Theme.instance().value_attr(False))

    def render(self) -> None:
        y,x = self.win.getbegyx()
        ym, xm = self.win.getmaxyx()
        self.paint_content_area_background()
        self.win.addstr(0, 0, self.label, Theme.instance().label_attr(self.has_focus))
        if self.has_focus:
            self.win.addstr(0, len(self.label), self.string_buffer.display_string, Theme.instance().value_attr(self.has_focus))
            self.position_cursor()
        else:
            self.win.addstr(0, len(self.label), self.string_buffer.display_string, Theme.instance().value_attr(self.has_focus))
            
        self.win.noutrefresh()

    def position_cursor(self) -> None:
        """
        Move the cursor to the current active position and makes sure it blinks.
        Should do nothing when this widget does not have focus
        """
        cur_attr = Theme.instance().cursor_attr()

        ch_under_cursor = self.string_buffer.display_string[self.string_buffer.cpos_buffer]
        if self.has_focus:
            self.win.addnstr(0, len(self.label) + self.string_buffer.cpos_buffer, ch_under_cursor, 1, cur_attr)
        # else:
        #     self.win.addnstr(0, len(self.label) + self.string_buffer.cpos_buffer, ch_under_cursor, 1,
        #                     curses.A_REVERSE + curses.A_BLINK)

        # self.win.noutrefresh()

    def focus_accept(self) -> None:
        """called by the app instance to give this control focus"""
        self.has_focus = True
        self.position_cursor()

    def focus_release(self) -> None:
        self.has_focus = False

    def get_key(self):
        return self.id

    def get_value(self) -> str:
        str_value = self.string_buffer.content
        return str_value

    def set_value(self, value):
        if type(value) == str:
            self.string_buffer.clear()
            self.string_buffer.add_string(value)
            pass
        else:
            raise ValueError("value is invalid type:{} value:{}".format(type(value), value))

    def handle_input(self, ch) -> bool:
        """
        When a Widget has the focus every keystroke (with some small exceptions)
        get passed to this function.
        If the Widget handles the keystroke then it should return true
        else should return false
        """
        did_handle_ch = True
        if (ch <= 255) and is_printable(ch) : 
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
    def __init__(self, app, key, label, width, data):
        super().__init__(app, key, label, width, data)

    def set_value(self, value):
        if type(value) == str :
            super().set_value(value)
        elif type(value) == int:
            super().set_value("{}".format(value))
        else:
            ValueError("value:{} of type {} is invalid".format(value, type(value)))


class FloatWidget(TextWidget):
    def __init__(self, app, key, label, width,  data):
        super().__init__(app, key, label, width,  data)

    def set_value(self, value):
        if type(value) == str :
            super().set_value(value)
        elif type(value) == float:
            super().set_value("{}".format(value))
        else:
            ValueError("value:{} of type {} is invalid".format(value, type(value)))


class IPAddressWidget(TextWidget):
    def __init__(self, app, key, label, width,  data):
        super().__init__(app, key, label, width,  data)

    def set_value(self, value):
        if type(value) == str :
            super().set_value(value)
        elif isinstance(value, ipaddress.IPv4Address) or isinstance(value, ipaddress.IPv6Address):
            super().set_value("{}".format(value))
        else:
            ValueError("value:{} of type {} is invalid".format(value, type(value)))


class IPNetworkWidget(TextWidget):
    def __init__(self, app, key, label, width,  data):
        super().__init__(app, key, label, width,  data)

    def set_value(self, value):
        if type(value) == str :
            super().set_value(value)
        elif isinstance(value, ipaddress.IPv4Network ) or isinstance(value, ipaddress.IPv6Network):
            super().set_value("{}".format(value))
        else:
            ValueError("value:{} of type {} is invalid".format(value, type(value)))


class TimeOfDayWidget(TextWidget):
    def __init__(self, app, key, label, width,  data): 
        super().__init__(app, key, label, width,  data)

    def set_value(self, value):
        if type(value) == str :
            super().set_value(value)
        elif isinstance(value, time.struct_time):
            super().set_value("{}".format(time.strf("%H:%M", value)))
        else:
            ValueError("value:{} of type {} is invalid".format(value, type(value)))


class PathWidget(TextWidget):
    def __init__(self, app, key, label, width,  data): 
        super().__init__(app, key, label, width,  data)

    def set_value(self, value):
        if type(value) == str :
            super().set_value(value)
        elif isinstance(value, pathlib.PosixPath):
            super().set_value("{}".format(value))
        else:
            ValueError("value:{} of type {} is invalid".format(value, type(value)))


class PathExistsWidget(TextWidget):
    def __init__(self, app, key, label, width,  data):
        super().__init__(app, key, label, width,  data)

    def set_value(self, value):
        if type(value) == str :
            super().set_value(value)
        elif isinstance(value, pathlib.PosixPath):
            super().set_value("{}".format(value))
        else:
            ValueError("value:{} of type {} is invalid".format(value, type(value)))

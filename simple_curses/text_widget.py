import curses
import curses.textpad
import time
import string

import string_buffer
import lines_buffer
from colors import Colors
import validator
from utils import *
from form import Form
from widget_base import WidgetBase

# A basic text widget that allows the entry of printable characters.
# A model upon which to base more complicated text controls
# A TextWidget is composed of a label and an value field
class TextWidget(WidgetBase):
    def __init__(self, relative_row, relative_col, key, label, width, attributes, data):
        self.id = key
        self.has_focus = False
        self.row = relative_row
        self.col = relative_col
        self.data = data
        # self.content = ""
        # self.content_position = 0
        self.label = label + ": "
        self.width = width
        self.height = 1
        self.start_row = 0
        self.start_col = 0

        self.attributes = attributes
        self.form = None
        self.validator = validator.Text()
        tmp = width + len(self.label)
        # self.win = curses.newwin(1, width + len(self.label) + 2, row, col, )
        self.string_buffer = string_buffer.StringBuffer("", self.width)

        # these properties are for manaing the display of the conttent string during
        # entry and editing
        self.display_content_start = 0
        self.display_content_position = 0 #current cursor position in the content
        self.display_cursor_position = 0 # always between 0 .. width - that is always visible
        self.display_length = 0 # is width-1 if we are adding to the end of the string in which case the cursor is over the 'next' slot
                                # if we are editing the string and the cursor is somewhere inside the content string then has the value width
    
    def set_enclosing_window(self, win: curses.window) -> None:
        self.win = win

    def set_form(self, form: Form) -> None:
        self.form = form


    def get_width(self) -> int:
        return len(self.label) + self.width + 2

    def get_height(self) -> int:
        return 1

    # paint attributes for the content area so that it is visible to used
    def paint_content_area_background(self) -> None:
        tmp = self.width + len(self.label) - 1
        for i in range(0, tmp):
            if self.has_focus:
                self.win.addstr(0, i, "_")
            else:
                self.win.addstr(0, i, "_")

    # called by the containing form to paint/render the Widget
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
        self.win.addnstr(0, len(self.label) + self.string_buffer.cpos_buffer, ch_under_cursor, 1, curses.A_REVERSE + curses.A_BLINK)
        self.win.noutrefresh()
    # 
    # called by the Form instance to give this control focus
    # 
    def focus_accept(self) -> None:
        self.has_focus = True
        self.position_cursor()

    def focus_release(self) -> None:
        self.has_focus = False

    def get_value(self) -> string:
        return self.string_buffer.content
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
    def handle_input(self, ch: string) -> bool:
        did_handle_ch = True
        if (len(ch)  == 1) and (ch[0] in string.printable):
            self.string_buffer.handle_character(ch)
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
    def __init__(self, row, col, key, label, width, attributes, data):
        super().__init__(row, col, key, label, width, attributes, data)
        self.validator = validator.Integer()

class FloatWidget(TextWidget):
    def __init__(self, row, col, key, label, width, attributes, data):
        super().__init__(row, col, key, label, width, attributes, data)
        self.validator = validator.Float()

class IPAddressWidget(TextWidget):
    def __init__(self, row, col, key, label, width, attributes, data):
        super().__init__(row, col, key, label, width, attributes, data)
        self.validator = validator.IPAddress()

class IPNetworkWidget(TextWidget):
    def __init__(self, row, col, key, label, width, attributes, data):
        super().__init__(row, col, key, label, width, attributes, data)
        self.validator = validator.IPNetwork()


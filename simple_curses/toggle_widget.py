import curses.textpad
from typing import List
from form import Form
from utils import *
from widget_base import EditableWidgetBase


# A widget that is either ON or OFF
class ToggleWidget(EditableWidgetBase):
    @classmethod
    def classmeth(cls):
        print("hello")

    def __init__(self, relative_row, relative_col, key, label, width, attributes, data, values: List[str], initial_value):

        def calc_width(svalues: List[str]):
            w = 0
            for v in svalues:
                w = len(v) if len(v) > w else w
            return w

        self.win = None
        self.id = key
        self.has_focus = False
        self.row = relative_row
        self.col = relative_col
        self.data = data
        self.content = values
        self.initial_value = initial_value
        try:
            self.current_index = values.index(initial_value)
        except ValueError:
            raise ValueError("initial_value {} is not list of possible values {}".format(initial_value, ", ".join(values)))
        self.label = label + ": "
        self.width = calc_width(values)
        self.height = 1
        self.start_row = 0
        self.start_col = 0

        self.attributes = attributes
        self.form = None

    def set_enclosing_window(self, win: curses.window) -> None:
        self.win = win

    def set_form(self, form: Form) -> None:
        self.form = form

    def get_width(self) -> int:
        return len(self.label) + self.width + 2

    def get_height(self) -> int:
        return 1

    def clear(self):
        self.content = False

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
        display = self.content[self.current_index]
        if self.has_focus:
            self.win.addstr(0, len(self.label), display, curses.A_REVERSE)
        else:
            self.win.addstr(0, len(self.label), display)

        self.win.noutrefresh()

    # 
    # Positions the cursor to the current active position and makes sure it blinks.
    # The current active position is usually 1 space past the end of the currently input text
    # 
    def position_cursor(self) -> None:
        ch_under_cursor = "Y" if self.content else "N"
        self.win.addnstr(0, len(self.label), ch_under_cursor, 1,
                         curses.A_REVERSE + curses.A_BOLD)
        self.win.noutrefresh()

    # 
    # called by the Form instance to give this control focus
    # 
    def focus_accept(self) -> None:
        self.has_focus = True
        self.position_cursor()

    def focus_release(self) -> None:
        self.has_focus = False

    def get_value(self) -> bool:
        return self.content

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
        if (ch <= 255) and (chr(ch) in ["\n", "\r", " "]):
            self.current_index = (self.current_index + 1) % 2
        else:
            did_handle_ch = False

        self.position_cursor()
        return did_handle_ch

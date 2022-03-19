import time
import sys
from abc import ABC, abstractmethod, abstractproperty
import curses
import curses.textpad
import time
from simple_curses.colors import Colors
from simple_curses.utils import *
from simple_curses.widget_base import WidgetBase

class MenuItem(WidgetBase):
    @classmethod
    def classmeth(cls):
        pass
    def __init__(self, relative_row, relative_col, label, width, height, attributes, function, context):
        self.label = label
        self.function = function
        self.context = context
        self.validator = None
        self.form = None
        self.win = None
        self.has_focus = False
        self.row = relative_row
        self.col = relative_col
        self.height = height
        self.width = width
        self.start_row = 0
        self.start_col = 0


    def set_enclosing_window(self, win: curses.window) -> None:
        self.win = win

    def set_form(self, aform) -> None:
        self.form = aform

    def get_width(self) -> int:
        return self.width + 4 if self.width > 4 else 12

    def get_height(self) -> int:
        return 3

    def position_cursor(self) -> None:
        pass

    def focus_accept(self) -> None:
        self.has_focus = True
    
    def focus_release(self) -> None:
        self.has_focus = False

    def handle_input(self, ch) -> None:
        did_handle_ch = True
        if is_return(ch) or is_space(ch) or is_linefeed(ch):
            self.invoke()
        else:
            did_handle_ch = False

        self.position_cursor()
        return did_handle_ch

    def invoke(self) -> None:
        self.function(self.form, self.context)
    
    def render(self) -> None:
        if self.has_focus:
            self.win.bkgd(" ", Colors.button_focus())
            self.win.addstr(1, 1, self.label, Colors.button_focus())
        else:
            self.win.bkgd(" ", Colors.button_no_focus())
            self.win.addstr(1, 1, self.label, Colors.button_no_focus())

        self.win.noutrefresh()


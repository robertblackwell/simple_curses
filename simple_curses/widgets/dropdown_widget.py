from typing import List
import curses.textpad
from simple_curses.keyboard import *
from simple_curses.widget_base import EditableWidgetBase
from simple_curses.theme import Theme


def calc_width(svalues):
    w = 0
    for v in svalues:
        w = len(v[1]) if len(v[1]) > w else w
    return w


class DropdownWidget(EditableWidgetBase):

    @classmethod
    def classmeth(cls):
        pass

    def __init__(self, app, key, label, width, height,  data, selections):
        """
        Dropdown constructor
        @param app    App
        @param key    str      Unique identifier for this instance of widget
        @param label  str      On screen descriptor
        @param width  int      Required width of the value part of the widget
        @param height int      Required height of the widget
        @param data   Any
        @param selection List[Tuple(int, str)]  A list of selections. 
                                                Each selection consists of str and an int 
                                                The string value is what is displayed in the drop down box
                                                the int value that is returned by the widgets get_value() method
        """
        self.content_win = None
        self.id: str = key
        self.has_focus: bool = False
        # self.row: int = row
        # self.col: int = col
        self.data = data
        self.label: str = label + ": "
        self.help_message = "Up/Down arrow keys for selection"
        self.width: int = calc_width(selections) +len(self.label) + 2 + len(self.help_message)
        self.selections = selections
        self.current_selection_index = 0
        self.height: int = height
        self.start_row: int = 0
        self.start_col: int = 0

        self.app = app
        self.win = None

    def set_enclosing_window(self, win):
        self.win = win

    # def focus_accept(self):
    #     self.has_focus = True

    # def focus_release(self):
    #     self.has_focus = False

    # def get_width(self):
    #     return self.width + len(self.label) + 2 + len(self.help_message)

    def get_key(self):
        return self.id

    def clear(self):
        self.mu_lines_buffer.clear()

    def get_value(self):
        return self.selections[self.current_selection_index][0]

    def set_value(self, value):
        if type(value) == str:
            ix = 0
            for item in self.selections:
                if item[1] == value:
                    self.current_selection_index = ix
                    return
            raise ValueError("value {} is not a valid dropdown selection".format(value))
        elif type(value) == int:
            ix = 0
            for item in self.selections:
                if item[0] == value:
                    self.current_selection_index = ix
                    return
            raise ValueError("value {} is not a valid dropdown selection".format(value))

    def render(self) -> None:
        self.win.clear()
        """called by the containing app to paint/render the Widget"""
        # self.paint_content_area_background()
        h, w = self.win.getmaxyx()
        self.win.addstr(0, 0, self.label, Theme.instance().label_attr(self.has_focus))
        display = self.selections[self.current_selection_index][1]
        if self.has_focus:
            self.win.addstr(0, len(self.label), display, Theme.instance().cursor_attr())
            self.win.addstr(0, len(self.label) + len(display) + 1, self.help_message, 
                Theme.instance().value_attr(self.has_focus))
        else:
            self.win.addstr(0, len(self.label), display, Theme.instance().value_attr(self.has_focus))
            # self.win.addstr(0, len(self.label) + len(display) + 1, "   ", 
            #     Theme.instance().value_attr(self.has_focus))

        self.win.noutrefresh()

    def handle_input(self, ch):
        did_handle = True
        if is_move_down(ch):
            self.current_selection_index = (self.current_selection_index + 1) % len(self.selections) 
        elif is_move_up(ch):
            self.current_selection_index = (self.current_selection_index - 1) % len(self.selections) 
        else:
            did_handle = False
        return did_handle

    def paste_mode_handle_input(self):
        pass

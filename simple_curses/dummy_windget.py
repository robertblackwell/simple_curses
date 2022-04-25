import curses
import curses.textpad

from simple_curses.theme import Theme
from .keyboard import *


class DummyWidget:
    def __init__(self, key, label, width, height,  data):
        self.id = key
        self.has_focus = False
        self.row = 0
        self.col = 0
        self.data = data
        self.label = label
        self.width = width
        self.height = height
        self.start_row = 0
        self.start_col = 0

        # self.attributes = attributes
        self.lines_view = None
        self.outter_win = None
        self.form = None
        self.color_pair = None

    def set_enclosing_window(self, win):
        self.outter_win = win

    def set_form(self, form):
        self.form = form

    def focus_accept(self):
        self.has_focus = True
        self.position_cursor()

    def focus_release(self):
        self.has_focus = False

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def render(self):
        self.outter_win.bkgd(" ", self.color_pair)
        for i in range(0, self.height):
            self.outter_win.addstr(i, 1, "label: {} line : {}".format(self.label, i)[0:self.width - 1])
        self.outter_win.noutrefresh()
        curses.doupdate()

    def handle_input(self, ch) -> bool:
        return False

    def position_cursor(self):
        self.outter_win.bkgd(" ", Theme.instance().label_attr(self.has_focus))
        self.outter_win.noutrefresh()
        curses.doupdate()


class DummyShortWidget(DummyWidget):
    def __init__(self, key, label, width, height, attributes, data):
        DummyWidget.__init__(self, key, label, width, height, attributes, data)

    def render(self):
        self.outter_win.bkgd(" ", self.color_pair)
        self.outter_win.addstr(0, 1, self.label)
        self.outter_win.noutrefresh()
        curses.doupdate()

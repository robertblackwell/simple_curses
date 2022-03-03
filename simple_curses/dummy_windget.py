import curses
import curses.textpad
from colors import Colors
from utils import *


class DummyWidget:
    def __init__(self, key, label, width, height, attributes, data):
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

        self.attributes = attributes
        self.lines_view = None
        self.outter_win = None
        self.form = None

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
        self.outter_win.bkgd(" ", Colors.button_focus())
        self.outter_win.noutrefresh()
        curses.doupdate()


    def handle_input(self, ch):
        return False

    def position_cursor(self):
        self.outter_win.bkgd(" ", Colors.button_focus())
        self.outter_win.noutrefresh()
        curses.doupdate()


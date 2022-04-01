import curses
import curses.textpad

from colors import Colors
from utils import *
from kurses_ex import make_subwin
from widget_base import WidgetBase


class TitleWidget(WidgetBase):
    def __init__(self, app, key, label, width, height, data):
        self.id = key
        self.has_focus = False
        self.data = data
        self.title = label
        self.width = len(label) + 2
        self.height = 1

        # self.attributes = attributes
        self.outter_win = None
        self.win = None
        self.app = app


    def set_enclosing_window(self, win):
        self.outter_win = win
        ym, xm = self.outter_win.getmaxyx()
        ybeg = (ym - self.width) // 2
        self.win = make_subwin(self.outter_win, 1, self.width, ybeg, 1)

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
        return
        self.win.addstr(0,0,self.title, curses.A_BOLD)
        self.outter_win.noutrefresh()

    def handle_input(self, ch):
        return False

    def position_cursor(self):
        self.outter_win.bkgd(" ", Colors.button_focus())
        self.outter_win.noutrefresh()
        curses.doupdate()


"""
This file implements a top menu bar which consists of a an Icon (pfgitlet enlarged text) followed by a list
of menu items that select which view is being shown in the body of an app's screen
"""
from pyfiglet import Figlet
from simple_curses.kurses_ex import make_subwin
from simple_curses.widget_base import WidgetBase, FocusableWidgetBase
from simple_curses.layout import TopmenuLayout
from simple_curses.theme import Theme
from simple_curses.colors import Colors
from simple_curses.keyboard import *
from typing import List


class FigletWidget(WidgetBase):
    def __init__(self, figlet_input:str):
        figlet = Figlet(font = "big")
        icon_text = figlet.renderText(figlet_input)
        icon_list = icon_text.split('\n')
        icon_list = ["", figlet_input, ""]
        self.icon = icon_list
        self.lines = []
        w = 0
        for line in self.icon:
            self.lines.append(line)
            w = len(line) if len(line) > w else w
        self.height = len(self.lines)
        self.width = w + 2
        self.win = None

    def get_height(self):
        return self.height 
    
    def get_width(self):
        return self.width 

    def set_enclosing_window(self, win) -> None:
        self.win = win

    def handle_input(self, ch) -> bool:
        did_handle_ch = True
        if is_return(ch) or is_space(ch) or is_linefeed(ch):
            self.invoke()
        else:
            did_handle_ch = False

        self.position_cursor()
        return did_handle_ch

    def render(self):
        def pad(line, length):
            while len(line) < length:
                line = line + " "
                if len(line) < length:
                    line = " " + line
            return line

        y, x = self.win.getbegyx()
        ym, xm = self.win.getmaxyx()
        # self.win.addstr(0, 0, "123456")
        # self.win.addstr(1, 0, "Two   ")
        # self.win.addstr(2, 0, "Three")
        # self.win.refresh()
        # return
        r = 0
        mlines = []
        for line in self.lines:
            # pad line to be xm wide
            s = pad(line, xm-1)
            self.win.addstr(r, 0, line)
            self.win.refresh()
            r += 1
        self.win.refresh()


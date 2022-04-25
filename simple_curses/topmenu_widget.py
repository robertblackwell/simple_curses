"""
This file implements a top menu bar which consists of a an Icon (pfgitlet enlarged text) followed by a list
of menu items that select which view is being shown in the body of an app's screen
"""
from pyfiglet import Figlet
from simple_curses.kurses_ex import make_subwin
from simple_curses.widget_base import WidgetBase, FocusableWidgetBase
from simple_curses.theme import Theme
from simple_curses.keyboard import *
from typing import List

class TopMenuWidget(WidgetBase):
    def __init__(self, app, ident: str, label: str, accelerator_key, view):
        self.app = app
        self.ident = ident
        self.label = label
        self.view = view
        self.height = 3
        self.width = 4 + len(label)
        self.has_focus = False
        self.win = None
        self.accelerator = accelerator_key

    def get_accelerator(self):
        return self.accelerator

    def get_view(self):
        return self.view

    def get_height(self):
        return self.height 
    
    def get_width(self):
        return self.width 

    def set_enclosing_window(self, win) -> None:
        self.win = win
        pass

    def focus_accept(self):
        self.has_focus = True

    def focus_release(self):
        self.has_focus = False

    def invoke(self):
        self.app.view_make_current(self.view)

    def handle_input(self, ch) -> bool:
        did_handle_ch = True
        if is_return(ch) or is_space(ch) or is_linefeed(ch):
            self.invoke()
        else:
            did_handle_ch = False

        return did_handle_ch

    def render(self) -> None:
        self.win.bkgd(" ", Theme.instance().label_attr(self.has_focus))
        self.win.addstr(1, 1, self.label, Theme.instance().label_attr(self.has_focus))
        self.win.refresh()


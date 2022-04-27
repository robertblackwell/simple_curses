"""
This file implements a top menu bar which consists of a an Icon (pfgitlet enlarged text) followed by a list
of menu items that select which view is being shown in the body of an app's screen
"""
from pyfiglet import Figlet
from simple_curses.kurses_ex import make_subwin
from simple_curses.widget_base import WidgetBase, MenuBase
from simple_curses.theme import Theme
from simple_curses.keyboard import *
from typing import List

class _MenuTrait(MenuBase):
    def __init__(self, app, ident, label, height, function_key):
        self.app = app
        self.ident = ident
        self.label = label + " " + self.app.function_keys.description(function_key)
        self.height = height
        self.function_key = function_key
        self.width = 2 + len(self.label)
        self.has_focus = False
        self.win = None

    def get_fkey(self):
        return self.function_key
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

class TopMenuWidget(_MenuTrait):
    def __init__(self, app, ident: str, label: str, height, function_key, view):
        super().__init__(app, ident, label, height, function_key)
        self.app.function_keys.add_fkey(function_key, self)
        self.view = view

    def get_view(self):
        return self.view

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

class MenuItem(_MenuTrait):
    def __init__(self, app, label, height, function_key, function, context):
        super().__init__(app, "", label, height, function_key)
        self.function = function
        self.context = context
        self.validator = None
        self.label = label + " " + self.app.function_keys.description(function_key)

    def handle_input(self, ch) -> bool:
        did_handle_ch = True
        if is_return(ch) or is_space(ch) or is_linefeed(ch):
            self.invoke()
        else:
            did_handle_ch = False

        self.position_cursor()
        return did_handle_ch

    def invoke(self) -> None:
        self.function(self.app, self.app.get_current_view())#, self.context)

    def render(self) -> None:
        self.win.bkgd(" ", Theme.instance().label_attr(self.has_focus))
        self.win.addstr(1, 1, self.label, Theme.instance().label_attr(self.has_focus))
        self.win.noutrefresh()


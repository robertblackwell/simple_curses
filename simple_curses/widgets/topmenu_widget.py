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

class TopMenuWidget(WidgetBase):
    def __init__(self, app, ident: str, label: str, height, accelerator_key, view):
        self.app = app
        self.accelerator = accelerator_key
        self.app.function_keys.add_accelerator(accelerator_key, self)
        self.ident = ident
        self.label = label + " " + self.app.function_keys.description(self.accelerator)
        self.view = view
        self.height = height
        self.width = 2 + len(self.label)
        self.has_focus = False
        self.win = None

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

class MenuItem(MenuBase):
    def __init__(self, app, label, height, accelerator_key, function, context):
        self.label = label
        self.function = function
        self.context = context
        self.validator = None
        self.app = app
        self.accelerator_key = accelerator_key
        # self.app.function_keys.add_accelerator(accelerator_key, self)
        self.label = label + " " + self.app.function_keys.description(accelerator_key)
        self.win = None
        self.has_focus = False
        self.height = height
        self.width = len(self.label) + 2
        self.start_row = 0
        self.start_col = 0

    def set_enclosing_window(self, win) -> None:
        self.win = win

    def get_width(self) -> int:
        return self.width + 4 if self.width > 4 else 12

    def get_height(self) -> int:
        return 3

    def get_accelerator_key(self):
        return self.accelerator_key

    def position_cursor(self) -> None:
        pass

    def focus_accept(self) -> None:
        self.has_focus = True

    def focus_release(self) -> None:
        self.has_focus = False

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
        # if self.has_focus:
        #     self.win.bkgd(" ", Theme.instance().label_attr(self.has_focus))
        #     self.win.addstr(1, 1, self.label, Theme.instance().label_attr(self.has_focus))
        # else:
        #     self.win.bkgd(" ", Theme.instance().label_attr(self.has_focus))
        #     self.win.addstr(1, 1, self.label, Theme.instance().label_attr(self.has_focus))

        self.win.noutrefresh()


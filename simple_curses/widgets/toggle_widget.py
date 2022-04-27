import curses.textpad
from typing import List

from simple_curses.keyboard import *
from simple_curses.validator import *
from simple_curses.widget_base import *
from simple_curses.theme import Theme 

class ToggleWidget(EditableWidgetBase):
    """A widget that is either ON or OFF"""
    
    def __init__(self, app, key, label, width, data, values: List[str]):

        def calc_width(svalues: List[str]):
            """calc width of the toggle strings"""
            w = 0
            for v in svalues:
                w = len(v) if len(v) > w else w
            return w

        # self.win: Union[None, curses.window] = None
        self.id = key
        self.has_focus = False
        self.data = data
        self.content = values
        self.current_index = 0 #index into values[]
        self.label = label + ": "
        self.help_message = "Hit space key to toggle"
        self.width = calc_width(values) #+ len(self.label) + len(self.help_message)
        self.height = 1
        self.start_row = 0
        self.start_col = 0
        self.app = app

    def set_enclosing_window(self, win) -> None:
        self.win = win

    def get_width(self) -> int:
        """TODO - fix this"""
        return len(self.label) + self.width + 2 + len(self.help_message)

    def clear(self):
        self.content = False

    def get_key(self):
        return self.id

    def get_value(self) -> bool:
        return self.current_index == 1

    def set_value(self, onoff):
        value = onoff
        if type(value) == str and onoff in self.content:
            self.current_index = self.content.index(onoff)
        elif type(value) == bool:
            self.current_index = 1 if onoff else 0
        elif type(value) == int and 0 <= onoff < len(self.content):
            self.current_index = onoff 
        else:
            raise ValueError("onoff is invalid {} {}".format(type(onoff), onoff))


    def paint_content_area_background(self) -> None:
        """paint attributes for the content area so that it is visible to used"""
        tmp = self.width# + len(self.label) - 1
        for i in range(0, tmp):
            if self.has_focus:
                self.win.addstr(0, i, "_")
            else:
                self.win.addstr(0, i, "_")

    def render(self) -> None:
        self.win.clear()
        """called by the containing app to paint/render the Widget"""
        self.paint_content_area_background()
        self.win.addstr(0, 0, self.label, Theme.instance().label_attr(self.has_focus))
        display = self.content[self.current_index]
        if self.has_focus:
            self.win.addstr(0, len(self.label), display, Theme.instance().cursor_attr())
            self.win.addstr(0, len(self.label) + len(display) + 1, self.help_message, 
                Theme.instance().value_attr(self.has_focus))
        else:
            self.win.addstr(0, len(self.label), display, Theme.instance().value_attr(self.has_focus))
            # self.win.addstr(0, len(self.label) + len(display) + 1, "   ", 
            #     Theme.instance().value_attr(self.has_focus))

        self.win.noutrefresh()

    def position_cursor(self) -> None:
        """ 
        Positions the cursor to the current active position and makes sure it blinks.
        The current active position is usually 1 space past the end of the currently input text
        """
        ch_under_cursor = "Y" if self.content else "N"
        self.win.addnstr(0, len(self.label), ch_under_cursor, 1,
                         curses.A_REVERSE + curses.A_BOLD)
        self.win.noutrefresh()

    # def focus_accept(self) -> None:
    #     """ 
    #     called by the app instance to give this control focus
    #     """ 
    #     self.has_focus = True

    # def focus_release(self) -> None:
    #     self.has_focus = False


    def handle_input(self, ch) -> bool:
        """
        When a Widget has the focus every keystroke (with some small exceptions)
        get passed to this function.
        If the Widget handles the keystroke then it should return true
        else should return false
        """ 
        did_handle_ch = True
        if (ch <= 255) and (chr(ch) in ["\n", "\r", " "]):
            self.current_index = (self.current_index + 1) % 2
        else:
            did_handle_ch = False

        return did_handle_ch

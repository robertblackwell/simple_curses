
import curses
import curses.textpad
from .colors import Colors
from .widget_base import MenuBase
from .utils import  is_return, is_space, is_linefeed

class DummyMenuItem(MenuBase):
    def __init__(self, app, label, width, height, attributes, function, context):
        self.label = label
        self.function = function
        self.context = context
        self.validator = None
        self.app = app
        self.win = None
        self.has_focus = False
        # self.row = relative_row
        # self.col = relative_col
        self.height = height
        self.width = width
        self.start_row = 0
        self.start_col = 0


    def set_enclosing_window(self, win: curses.window) -> None:
        self.win = win

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

    def handle_input(self, ch) -> bool:
        did_handle_ch = True
        if is_return(ch) or is_space(ch) or is_linefeed(ch):
            self.invoke()
        else:
            did_handle_ch = False

        self.position_cursor()
        return did_handle_ch

    def invoke(self) -> None:
        self.function(self.app, self.context)
    
    def render(self) -> None:
        if self.has_focus:
            self.win.bkgd(" ", Colors.button_focus())
            self.win.addstr(1, 1, self.label, Colors.button_focus())
        else:
            self.win.bkgd(" ", Colors.button_no_focus())
            self.win.addstr(1, 1, self.label, Colors.button_no_focus())

        self.win.noutrefresh()


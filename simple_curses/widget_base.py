from abc import ABC, abstractmethod, abstractproperty
import curses
import curses.textpad
from colors import Colors
from utils import *

class WidgetBase:#(ABC):
    """A basic widget that can display fixed text on the screen"""

    # @classmethod
    # @abstractmethod
    # def classmeth(cls):
    #     pass

    # @abstractmethod
    # def foobar(self):
    #     pass

    @abstractmethod
    def get_height(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def get_width(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def render(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def handle_input(self, ch) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def set_enclosing_window(self, win: curses.window) -> None:
        raise NotImplementedError()

    def set_parent_view(self, view):
        self.parent_view = view


class FocusableWidgetBase(WidgetBase):
    """A widget that can accept the focus and may be able to navigate around its fixed text display"""

    @abstractmethod
    def focus_accept(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def focus_release(self) -> None:
        raise NotImplementedError()


class EditableWidgetBase(FocusableWidgetBase):
    """A widget that contains one of more variable fields that can be edited by the user"""

    @abstractmethod
    def get_value(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError()


class MenuBase(FocusableWidgetBase):
    "A widget that can accept the focus, cannot be edited, but can be 'invoked' to call an action function"

    @abstractmethod
    def invoke(self):
        raise NotImplementedError()

class MenuItem(MenuBase):
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

    def handle_input(self, ch) -> None:
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



def is_widget(w):
    return callable(getattr(w, "get_height")) \
        and callable(getattr(w, "get_width")) \
        and callable(getattr(w, "render")) \
        and callable(getattr(w, "set_enclosing_window")) \
        and callable(getattr(w, "handle_input"))


def is_focusable(widget):
    return callable(getattr(widget, "focus_accept")) and callable(getattr(widget, "focus_release"))

def is_editable(widget):
    return is_focusable(widget) and callable(getattr(widget, "get_values")) and callable(getattr(widget, "clear"))

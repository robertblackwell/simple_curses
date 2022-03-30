from abc import ABC, abstractmethod, abstractproperty
import curses
import curses.textpad
from colors import Colors
from utils import *
from multi_line_buffer import MultiLineBuffer
from kurses_ex import *

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

    def get_key(self) -> str:
        raise NotImplementedError()


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
    def set_value(self, v) -> str:
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
        self.function(self.app, self.app.get_current_view(), self.context)
    
    def render(self) -> None:
        if self.has_focus:
            self.win.bkgd(" ", Colors.button_focus())
            self.win.addstr(1, 1, self.label, Colors.button_focus())
        else:
            self.win.bkgd(" ", Colors.button_no_focus())
            self.win.addstr(1, 1, self.label, Colors.button_no_focus())

        self.win.noutrefresh()

xlines = [
    "0  01-1lkjhasdfhlakjsfhlajhflakdhjfldask",
    "1  02-1lkjhasdfhlakjsfhlajhflakdhjfldask",
    "2  03-1lkjhasdfhlakjsfhlajhflakdhjfldask",
    "3  04-1lkjhasdfhlakjsfhlajhflakdhjfldask",
    "4  05-1lkjhasdfhlakjsfhlajhflakdhjfldask",
    "5  06-1lkjhasdfhlakjsfhlajhflakdhjfldask",
    "6  07-1lkjhasdfhlakjsfhlajhflakdhjfldask",
    "7  08-1lkjhasdfhlakjsfhlajhflakdhjfldask",
    "8  09-1lkjhasdfhlakjsfhlajhflakdhjfldask",
    "9  10-1lkjhasdfhlakjsfhlajhflakdhjfldask",
    "A  0A-1lkjhasdfhlakjsfhlajhflakdhjfldask",
    "B  0B-1lkjhasdfhlakjsfhlajhflakdhjfldask",
    "C  0C-1lkjhasdfhlakjsfhlajhflakdhjfldask",
    "D  0D-1lkjhasdfhlakjsfhlajhflakdhjfldask",
    "E  0E-1lkjhasdfhlakjsfhlajhflakdhjfldask",
    "F  0F-1lkjhasdfhlakjsfhlajhflakdhjfldask",
    "10 10-1lkjhasdfhlakjsfhlajhflakdhjfldask",
    "11 11-1lkjhasdfhlakjsfhlajhflakdhjfldask",
]

class DummyMultiLineWidget(EditableWidgetBase):

    @classmethod
    def classmeth(cls):
        pass

    def __init__(self, app, key:str, label:str, content_width:int, content_height:int, data:any):
        self.info_win = None
        self.content_win = None
        self.line_number_win = None
        self.id: str = key
        self.has_focus: bool = False
        # self.row: int = row
        # self.col: int = col
        self.data = data
        self.label: str = label
        self.content_width = content_width
        self.width: int = content_width + 2
        self.line_number_width: int = 4
        # A multiline widget consists of :
        # - an outter box
        # - a title in the middile of the top box line
        # - a content area of height equal to the content_height argument
        # - a separator line bwteen the content area and the info area
        # - an info area of 4 lines 
        self.box_height = 2 #extra height for boxing the outter of the widget
        self.info_separator_line_height = 1 # extra height for the divider line between the content and the info box
        self.info_area_height = 4
        self.content_height = content_height
        self.height: int = content_height + self.box_height + self.info_separator_line_height + self.info_area_height 
        self.start_row: int = 0
        self.start_col: int = 0
        self.paste_mode: bool = False

        # self.attributes = attributes
        self.lines_view = None
        self.outter_win = None
        self.app = app
        self.mu_lines_buffer: MultiLineBuffer = MultiLineBuffer(xlines, self.content_height, self.content_width - self.line_number_width - 2)
    
   
    def set_enclosing_window(self, win):
        self.outter_win = win
        self.line_number_win = make_subwin(self.outter_win, self.content_height, self.line_number_width, 1, 1)
        self.content_win = make_subwin(self.outter_win, self.content_height, self.content_width - self.line_number_width, 1, self.line_number_width)
        self.info_win = make_subwin(self.outter_win, self.info_area_height, self.content_width, self.content_height + 1, 1)

    # def set_app(self, app: app):
    #     self.app = app

    def add_line(self, line: str):
        self.mu_lines_buffer.append_line(line)

    def focus_accept(self):
        self.has_focus = True
        # self.position_cursor()

    def focus_release(self):
        self.has_focus = False
        pass

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def clear(self):
        self.mu_lines_buffer.clear()

    def get_value(self):
        return self.mu_lines_buffer.get_value()

    def set_value(self, value):
        self.clear()
        if type(value) is list:
            for ln in value:
                self.add_line(ln) 
        pass

    def render_title(self):
        """Print the title in the middle of the top row - inside the top line of the box"""
        tl = len(self.label)
        t_x_begin = (self.width - tl) // 2
        self.outter_win.addstr(0, t_x_begin, self.label)

    def render_info(self):
        """render the info box underneath the list of strings. The box outline
        should merge witht he box of the content window"""
        self.info_win.bkgd(" ", Colors.white_black())
        # self.info_win.border(0, 0, 0, 0, curses.ACS_LTEE, curses.ACS_RTEE, 0, 0)
        self.info_win.addstr(1, 3, "Navigate these lines with arrow keys ".format(self.paste_mode), curses.A_BOLD)
        self.info_win.addstr(2, 3, "Type characters or Paste to insert.", curses.A_BOLD)
        self.info_win.addstr(3, 3, "Del and BS keys to delete", curses.A_BOLD)
        pass

    def render(self):
        self.outter_win.clear()
        self.outter_win.box()
        # self.outter_win.border(0, 0, 0, 0, 0, 0, curses.ACS_LTEE, curses.ACS_RTEE)
        self.render_title()

        view = self.mu_lines_buffer.get_view()
        y0 = view.view_content_y_begin
        y1 = view.view_content_y_end + 1
        r = 0
        for y_content in range(y0, y1):
            txt = view.view_buffer[r]
            line_number = view.line_numbers[r]
            ln_str = "{0:>2} ".format(line_number)
            y1m, x1m = self.content_win.getmaxyx()
            y2m, x2m = self.line_number_win.getmaxyx()
            self.content_win.addstr(r, 0, txt, Colors.green_black())
            self.line_number_win.addstr(r, 0, ln_str, Colors.white_black())
            if view.cpos_y_buffer == r and self.has_focus:
                self.content_win.addstr(r, view.cpos_x_buffer, view.char_under_cursor,
                                        Colors.green_black() + curses.A_REVERSE + curses.A_STANDOUT)
            r += 1

        self.render_info()
        self.outter_win.noutrefresh()
        self.content_win.noutrefresh()
        self.line_number_win.noutrefresh()
        self.info_win.noutrefresh()
        curses.doupdate()

    def handle_input(self, ch):
        did_handle = True
        if is_addline(ch):
            self.mu_lines_buffer.handle_add_line()
        elif is_cntrl_p(ch):
            self.toggle_paste_mode()
        elif is_edit_back(ch):
            self.set_paste_mode_off()
            self.mu_lines_buffer.handle_backspace()
        elif is_printable(ch) and (not is_newline(ch)):
            self.set_paste_mode_off()
            self.mu_lines_buffer.handle_character(chr(ch))
        elif is_edit_del(ch):
            self.set_paste_mode_off()
            self.mu_lines_buffer.handle_delete()
        elif is_delete_line(ch):
            self.set_paste_mode_off()
            self.mu_lines_buffer.handle_delete_line()
        elif is_move_down(ch):
            self.set_paste_mode_off()
            self.mu_lines_buffer.handle_down()
        elif is_move_left(ch):
            self.set_paste_mode_off()
            self.mu_lines_buffer.handle_left()
        elif is_move_right(ch):
            self.set_paste_mode_off()
            self.mu_lines_buffer.handle_right()
        elif is_move_up(ch):
            self.set_paste_mode_off()
            self.mu_lines_buffer.handle_up()
        elif is_newline(ch):
            self.set_paste_mode_off()
            self.mu_lines_buffer.handle_newline()
        else:
            did_handle = False

        # self.position_cursor()
        return did_handle

    def paste_mode_handle_input(self):
        pass

    ############################################################################################################
    # paste mode
    ############################################################################################################
    def toggle_paste_mode(self):
        before = self.paste_mode
        after = not self.paste_mode
        self.set_paste_mode(after)
        self.app.msg_info("toggle_paste_mode from:{} to:{}".format(before, after))

    def set_paste_mode(self, on_off):
        if on_off:
            self.set_paste_mode_on()
        else:
            self.set_paste_mode_off()

    def set_paste_mode_off(self):
        self.paste_mode = False

    def set_paste_mode_on(self):
        self.paste_mode = True
        self.mu_lines_buffer.cursor_set_at_end()
        self.mu_lines_buffer.handle_newline()
        self.paste_mode = True


def is_widget(w):
    x0 = isinstance(w, WidgetBase)
    return x0
    return hasattr(w, "get_height") \
        and callable(getattr(w, "get_height")) \
        and hasattr(w, "get_width") \
        and callable(getattr(w, "get_width")) \
        and hasattr(w, "get_width") \
        and callable(getattr(w, "render")) \
        and hasattr(w, "render") \
        and callable(getattr(w, "set_enclosing_window")) \
        and hasattr(w, "handle_input") \
        and callable(getattr(w, "handle_input"))


def is_focusable(widget):
    x0 = isinstance(widget, FocusableWidgetBase) or isinstance(widget, EditableWidgetBase)
    return x0
    x0 = hasattr(widget, "focus_accept") and callable(getattr(widget, "focus_accept")) 
    x1 = hasattr(widget, "focus_relase") and callable(getattr(widget, "focus_release"))
    return hasattr(widget, "focus_accept") and callable(getattr(widget, "focus_accept")) and hasattr(widget, "focus_relase") and callable(getattr(widget, "focus_release"))

def is_editable(widget):
    x0 = isinstance(widget, EditableWidgetBase)
    return x0
    x0 = is_focusable(widget)
    x1 = hasattr(widget, "get_value") and callable(getattr(widget, "get_value"))
    x2 = hasattr(widget, "clear") and callable(getattr(widget, "clear"))
    res = is_focusable(widget) and hasattr(widget, "get_value") and callable(getattr(widget, "get_value")) and hasattr(widget, "clear") and callable(getattr(widget, "clear"))
    return res
import curses
import curses.textpad
from typing import List, Any

from simple_curses.keyboard import *
from simple_curses.widget_base import WidgetBase, EditableWidgetBase
from simple_curses.kurses_ex import make_subwin
from simple_curses.theme import Theme
from simple_curses.widgets.multi_line_buffer import MultiLineBuffer

class MultiLineWidget(EditableWidgetBase):
    """
    A multiline widget consists of :
    -    an outter box
    -    a title in the middile of the top box line
    -    a content area of height equal to the content_height argument
    -    a separator line bwteen the content area and the info area
    -    an info area of N lines - edit the code to change N 
    """
    @classmethod
    def classmeth(cls):
        pass

    def __init__(self, app, key:str, label:str, content_width:int, content_height:int, data:Any):
        self.info_win = None
        self.content_win = None
        self.line_number_win = None
        self.id: str = key
        self.has_focus: bool = False
        self.data = data
        self.label: str = label
        self.content_width = content_width
        self.width: int = content_width + 2
        self.line_number_width: int = 4
        self.box_height = 2 #extra height for boxing the outter of the widget
        self.info_separator_line_height = 1 # extra height for the divider line between the content and the info box
        self.info_area_height = 4
        self.content_height = content_height
        self.height: int = content_height + self.box_height + self.info_separator_line_height + self.info_area_height 
        self.start_row: int = 0
        self.start_col: int = 0
        self.paste_mode: bool = False

        self.app = app
        self.mu_lines_buffer: MultiLineBuffer = MultiLineBuffer([], self.content_height, self.content_width - self.line_number_width - 2)
        self.lines_view = None
        self.outter_win = None
    
   
    def set_enclosing_window(self, win):
        self.outter_win = win
        self.line_number_win = make_subwin(self.outter_win, self.content_height, self.line_number_width, 1, 1)
        self.content_win = make_subwin(self.outter_win, self.content_height, self.content_width - self.line_number_width, 1, self.line_number_width)
        self.info_win = make_subwin(self.outter_win, self.info_area_height, self.content_width, self.content_height + 1, 1)

    def add_line(self, line: str):
        self.mu_lines_buffer.append_line(line)

    def clear(self):
        self.mu_lines_buffer.clear()

    def get_key(self) -> str:
        return self.id

    def get_value(self) -> List[str]:
        """Returns the values in the widget in the form of list of strings"""
        values = self.mu_lines_buffer.get_value()
        str_result = [] if len(values) == 1 and values[0] == "" else values
        return str_result

    def set_value(self, value: List[str]):
        """Sets the values in the widget - expects a List of strings"""
        self.clear()
        if type(value) is list:
            for ln in value:
                self.add_line(ln) 
        pass

    def render_title(self):
        """Print the title in the middle of the top row - inside the top line of the box"""
        tl = len(self.label)
        t_x_begin = (self.width - tl) // 2
        self.outter_win.addstr(0, t_x_begin, self.label, Theme.instance().label_attr(self.has_focus))

    def render_info(self):
        """render the info box underneath the list of strings. The box outline
        should merge witht he box of the content window"""
        self.info_win.bkgd(" ", Theme.instance().label_attr(self.has_focus))
        # self.info_win.border(0, 0, 0, 0, curses.ACS_LTEE, curses.ACS_RTEE, 0, 0)
        self.info_win.addstr(1, 3, "Navigate these lines with arrow keys ", Theme.instance().label_attr(self.has_focus))
        self.info_win.addstr(2, 3, "Type characters or Paste to insert.", Theme.instance().label_attr(self.has_focus))
        self.info_win.addstr(3, 3, "Del and BS keys to delete", Theme.instance().label_attr(self.has_focus))
        pass

    def render(self):
        self.outter_win.clear()
        self.outter_win.attron(Theme.instance().label_attr(self.has_focus))
        self.outter_win.box()
        self.outter_win.attron(Theme.instance().label_attr(self.has_focus))

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
            self.content_win.addstr(r, 0, txt,  Theme.instance().value_attr(self.has_focus))
            self.line_number_win.addstr(r, 0, ln_str, Theme.instance().value_attr(False))
            if view.cpos_y_buffer == r and self.has_focus:
                self.content_win.addstr(r, view.cpos_x_buffer, view.char_under_cursor,
                                        Theme.instance().cursor_attr())
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
        elif is_edit_back(ch):
            self.mu_lines_buffer.handle_backspace()
        elif is_printable(ch) and (not is_newline(ch)):
            self.mu_lines_buffer.handle_character(chr(ch))
        elif is_edit_del(ch):
            self.mu_lines_buffer.handle_delete()
        elif is_delete_line(ch):
            self.mu_lines_buffer.handle_delete_line()
        elif is_move_down(ch):
            self.mu_lines_buffer.handle_down()
        elif is_move_left(ch):
            self.mu_lines_buffer.handle_left()
        elif is_move_right(ch):
            self.mu_lines_buffer.handle_right()
        elif is_move_up(ch):
            self.mu_lines_buffer.handle_up()
        elif is_newline(ch):
            self.mu_lines_buffer.handle_newline()
        else:
            did_handle = False

        return did_handle

    def paste_mode_handle_input(self):
        pass

class IPNetworkCIDR(MultiLineWidget):
    def __init__(self, app, key:str, label:str, content_width:int, content_height:int, data:Any):
        super().__init__(app, key, label, content_width, content_height, data)
        # self.validator = validator.ArrayOf(validator.IPNetwork())

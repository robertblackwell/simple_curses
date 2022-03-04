import curses
import curses.textpad
import lines_buffer
from colors import Colors
from utils import *
from simple_curses.widget_base import WidgetBase
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

class ScrollingWidget(WidgetBase):
    def __init__(self, row, col, key, label, width, height, attributes, data):
        self.id = key
        self.has_focus = False
        self.row = row
        self.col = col
        self.data = data
        self.label = label + ": "
        self.width = width
        self.height = height
        self.start_row = 0
        self.start_col = 0

        self.attributes = attributes
        self.lines_view = None
        self.outter_win = None
        self.form = None
        tmp = width + len(self.label)
        self.lines_buffer = lines_buffer.LinesBuffer(xlines, 0, self.height - 3)

        # these properties are for manaing the display of the conttent string during
        # entry and editing
        self.display_content_start = 0
        self.display_content_position = 0 #current cursor position in the content
        self.display_cursor_position = 0 # always between 0 .. width - that is always visible
        self.display_length = 0 # is width-1 if we are adding to the end of the string in which case the cursor is over the 'next' slot

    def set_enclosing_window(self, win):
        self.outter_win = win
        x = self.outter_win.getmaxyx()
        self.title_window = curses.newwin(1, self.width, self.start_row, self.start_col)
        self.content_win = curses.newwin(self.height - 2,  self.width - 3, self.start_row + 1, self.start_col + 1)

    def set_form(self, form):
        self.form = form


    def add_line(self, line):
        self.lines_buffer.append_line(line)

    def focus_accept(self):
        self.has_focus = True
        self.position_cursor()

    def focus_release(self):
        self.has_focus = False
        pass

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def render(self):
        self.outter_win.box()
        # self.outter_win.bkgd(" ", Colors.button_focus())
        
        t_c = (self.width - len(self.label)) // 2
        self.title_window.addstr(0, t_c, self.label, curses.A_BOLD)
        if self.has_focus:
            self.content_win.bkgd(" ", Colors.button_no_focus())
            self.content_win.addstr(0, 0, "ABCDEF")
        else:
            self.content_win.bkgd(" ", Colors.button_no_focus())
            self.content_win.addstr(0, 0, "ABCDEF")

        lines = self.lines_buffer.get_view()
        r = 0
        # for rw in range(self.height):

        for line in lines:
            txt = "{0:<4} {1:}".format(line[0], line[1])
            if self.has_focus and r == self.lines_buffer.cpos_view:
                self.content_win.addstr(r, 0, txt, Colors.button_focus())
            else:
                self.content_win.addstr(r, 0, txt, Colors.button_no_focus())
            r += 1



        # if self.has_focus:
        #     self.position_cursor()
        self.outter_win.noutrefresh()
        self.title_window.noutrefresh()
        self.content_win.noutrefresh()
        curses.doupdate()

    def handle_input(self, ch):
        did_handle = True
        if is_move_down(ch):
            self.lines_buffer.handle_down()
        elif is_move_up(ch):
            self.lines_buffer.handle_up()
        else:
            did_handle = False
        self.position_cursor()
        return did_handle

    def position_cursor(self):
        cpos_buffer = self.lines_buffer.cpos_view
        tmp = self.lines_buffer.lines[self.lines_buffer.cpos_lines]
        text = "{}:{}".format(tmp[0], tmp[1])
        self.content_win.addstr(cpos_buffer, 0, text, Colors.button_focus())
        self.content_win.noutrefresh()
        curses.doupdate()


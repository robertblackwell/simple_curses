import curses
import curses.textpad
import lines_buffer
from colors import Colors
from utils import *
from simple_curses.widget_base import WidgetBase
from multi_line_buffer import MultiLineBuffer
from simple_curses.menu import MenuItem
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

class MultiLineWidget(WidgetBase):

    @classmethod
    def classmeth(cls):
        pass

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
        self.paste_mode = False

        self.attributes = attributes
        self.lines_view = None
        self.outter_win = None
        self.form = None
        tmp = width + len(self.label)
        self.mu_lines_buffer: MultiLineBuffer = MultiLineBuffer(xlines, self.height - 2, self.width)


        # these properties are for manaing the display of the conttent string during
        # entry and editing
        # self.display_content_start = 0
        # self.display_content_position = 0 #current cursor position in the content
        # self.display_cursor_position = 0 # always between 0 .. width - that is always visible
        # self.display_length = 0 # is width-1 if we are adding to the end of the string in which case the cursor is over the 'next' slot

    def set_enclosing_window(self, win):
        self.outter_win = win
        x = self.outter_win.getmaxyx()
        self.title_window = curses.newwin(1, self.width, self.start_row, self.start_col)
        self.line_number_win = curses.newwin(self.height - 2, 3, self.start_row + 1, self.start_col + 1)
        self.content_win = curses.newwin(self.height - 1,  self.width - 3, self.start_row + 1, self.start_col + 1 + 3)
        self.info_win = curses.newwin(4, self.width, self.start_row + self.height - 2 + 1, self.start_col)
        # self.paste_menu_item =  MenuItem(self.start_row + 1, 1, "PasteOn", 13, 3, 0, self.menuAction1, "context for menu 1")

    def menuAction1(self):
        pass

    def set_form(self, form):
        self.form = form


    def add_line(self, line):
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



    def render(self):
        # self.outter_win.box()
        self.outter_win.border(0, 0, 0, 0, 0, 0, curses.ACS_LTEE, curses.ACS_RTEE)
        self.info_win.border(0, 0, 0, 0, curses.ACS_LTEE, curses.ACS_RTEE, 0, 0)
        # self.info_win.box()
        # self.outter_win.bkgd(" ", Colors.button_focus())
        
        # t_c = (self.width - len(self.label)) // 2
        # self.title_window.addstr(0, t_c, self.label, curses.A_BOLD)
        # if self.has_focus:
        #     self.content_win.bkgd(" ", Colors.button_no_focus())
        #     self.content_win.addstr(0, 0, "ABCDEF")
        # else:
        #     self.content_win.bkgd(" ", Colors.button_no_focus())
        #     self.content_win.addstr(0, 0, "ABCDEF")

        # for rw in range(self.height):
        y0 = self.mu_lines_buffer.view_y_begin
        y1 = self.mu_lines_buffer.view_y_end + 1
        x0 = self.mu_lines_buffer.view_x_begin
        x1 = self.mu_lines_buffer.view_x_end + 1
        y_curs = self.mu_lines_buffer.cpos_y_content
        x_curs = self.mu_lines_buffer.cpos_x_content
        cursor_ch = "X"
        if x_curs <  len(self.mu_lines_buffer.content[y_curs]):
            cursor_ch = self.mu_lines_buffer.content[y_curs][x_curs]
        y_curs_buf = self.mu_lines_buffer.cpos_y_buffer
        x_curs_buf = self.mu_lines_buffer.cpos_x_buffer

        vstr = self.mu_lines_buffer.get_view()
        r = 0
        for ln in range(y0, y1):
            s = self.mu_lines_buffer.content[ln][x0: x1]
            s = vstr.lines[r]
            txt = "{}".format(s)
            line_number = vstr.one_based_line_numbers[r]
            ln_str = "{}".format(line_number)
            self.content_win.addstr(r, 0, txt, Colors.green_black())
            self.line_number_win.addstr(r, 0, ln_str, Colors.white_black())
            if y_curs_buf == r and self.has_focus:
                assert y_curs_buf == vstr.curs_y
                assert x_curs_buf == vstr.curs_x
                
                self.content_win.addstr(r, x_curs_buf, cursor_ch, Colors.green_black() + curses.A_REVERSE + curses.A_STANDOUT)
            r += 1

        self.info_win.bkgd(" ", Colors.green_black() + curses.A_BOLD)
        self.info_win.addstr(1, 3, "Paste Mode: {} ".format(self.paste_mode))
        self.info_win.addstr(2, 3, "Cntrl-p toggles paste mode")

        # for line in lines:
        #     # txt = "{0:<4} {1:}".format(line[0], line[1])
        #     txt = "{}".format(line[1])
        #     if self.has_focus and r == self.mu_lines_buffer.cpos_view:
        #         self.content_win.addstr(r, 0, txt, Colors.button_focus())
        #     else:
        #         self.content_win.addstr(r, 0, txt, Colors.button_no_focus())
        #     r += 1



        # if self.has_focus:
        #     self.position_cursor()
        self.outter_win.noutrefresh()
        self.title_window.noutrefresh()
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
        elif (len(ch)  == 1) and (ch[0] in string.printable) and not ch == "\n":
            self.set_paste_mode_off()
            self.mu_lines_buffer.handle_character(ch)
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
        self.form.msg_info("toggle_paste_mode from:{} to:{}".format(before, after))

    def set_paste_mode(self, on_off):
        if on_off:
            self.set_paste_mode_on()
        else:
            self.set_paste_mode_off()

    def set_paste_mode_off(self):
        self.paste_mode = False

    def set_paste_mode_on(self):
        self.paste_mode = True
        self.mu_lines_buffer._cursor_set_at_end()
        self.mu_lines_buffer.handle_newline()
        self.paste_mode = True

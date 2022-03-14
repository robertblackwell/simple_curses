import curses
import curses.textpad
import string
from datetime import datetime

import string_buffer
from colors import Colors

def is_next_control(ch):
    return (ch == "KEY_RIGHT" or ch == curses.KEY_RIGHT)

def is_prev_control(ch):
    return (ch == "KEY_LEFT" or ch == curses.KEY_LEFT)

def is_function_key(ch):
    tmp = ch[0:6]
    return (tmp == "KEY_F(")

def fn_key_match(k1, k2):
    return (k1 == k2)

def fn_key_description(k1):
    s1 = k1.replace("KEY_F(", "")
    s2 = s1.replace(")", "")
    s3 = "F"+s2
    return s3


class Form:
    def __init__(self, stdscr, height, width, widgets, context):
        self.height = height
        self.width = width
        self.widgets = widgets
        self.context = context
        self.stdscr = stdscr
        self.focus_index = 0
        self.title = "This is a data entry form"

        self.menu_height = 5
        self.msg_height = 10
        self.title_height = 5
        self.body_height = self.height - self.title_height - self.msg_height + 2

        self.title_start_row = 0
        self.title_start_col = 0
        self.title_width = self.width
        self.outter_win = curses.newwin(self.height + 2, self.width + 2, 0, 0)
        self.inner_win = self.outter_win.subwin(self.height, self.width, 1, 1)
        self.title_win = curses.newwin(self.title_height, self.title_width, 0, 0)


        self.body_start_row = self.title_start_row + self.title_height
        self.body_start_col = 0
        self.body_width = self.width

        self.menu_start_row = self.body_start_row + self.body_height - 1
        self.menu_width = self.width

        self.msg_start_row = self.menu_start_row + self.menu_height - 1
        self.msg_width = self.width

        body_start_row = self.body_start_row #4
        body_start_col = 0

        self.messages = []
        self.msg_count = 0

        self.body_win = curses.newwin(self.body_height, self.width, self.body_start_row, 0 )
        # self.body_win.bkgd(" ", Colors.button_no_focus())
        self.msg_win = curses.newwin(self.msg_height, self.msg_width, self.msg_start_row, 0 )
        self.menu_win = curses.newwin(self.menu_height, self.menu_width, self.menu_start_row, 0)
        # self.msg_win.bkgd(" ", Colors.button_focus())
        self.message_text = ""
        body_height = 0
        col = body_start_col + 4  
        for w in self.widgets:
            klass = w.__class__.__name__
            if klass == "MenuItem":
                w.set_enclosing_window(curses.newwin(w.get_height(), w.get_width(), w.row, col + 1))
                col += w.get_width() + 4
            else:
                w.start_row = w.row + body_start_row
                w.start_col = w.col + body_start_col
                w.set_enclosing_window(curses.newwin(w.get_height(), w.get_width(), self.body_start_row + w.row, self.body_start_col + w.col ))
            w.set_form(self)
            w.has_focus = False
        zz = self.body_win.getparyx()
        z2 = self.title_win.getparyx()
        z3 = z2

    def msg(self, label, msg, attr):
        self.msg_count += 1
        self.messages.append([self.msg_count, label, msg, attr])
        self.msg_win.clear()
        count = 1
        r = 1
        index = len(self.messages) - 1
        while index >= 0 and count < self.msg_height-1 and r < self.msg_height-1:
            str = "  {}:{}:{}".format(self.messages[index][0], self.messages[index][1], self.messages[index][2])
            if len(str) > self.msg_width - 5:
                str = str[0:self.msg_width - 5]
            else:
                str.ljust(self.msg_width - 5)
            self.msg_win.addstr(r, 0, str, self.messages[index][3])
            index += -1
            count += 1
            r += 1
        
        self.msg_win.noutrefresh()
        curses.doupdate()

    def msg_error(self, msg):
        label = " ERROR: "
        self.msg(label, msg, Colors.msg_error_attr())

    def msg_warn(self, msg):
        label = " WARNING: "
        self.msg(label, msg, Colors.msg_warn_attr())

    def msg_info(self, msg):
        label = " INFO: "
        self.msg(label, msg, Colors.msg_info_attr())

    def handle_input(self):
        # here should render everything to ensure the latest version of the screen is being seen
        # hen input is provided
        # ch = self.stdscr.getkey()
        ch = self.stdscr.getch()
        chstr = chr(ch) if ch <= 255 else hex(ch)

        self.msg_info("handle_input ch: {} hex: {}".format(chstr, hex(ch)))
        focus_widget = self.widgets[self.focus_index]
        focus_widget.focus_accept()
        if focus_widget.handle_input(ch):
            return
        else:
            if is_next_control(ch):
                old_focus_widget = self.widgets[self.focus_index]
                self.focus_index = (self.focus_index + 1 + len(self.widgets)) % (len(self.widgets))
                old_focus_widget.focus_release()
                focus_widget = self.widgets[self.focus_index]
                focus_widget.focus_accept()
            elif is_prev_control(ch):
                old_focus_widget = self.widgets[self.focus_index]
                self.focus_index = (self.focus_index - 1 + len(self.widgets)) % (len(self.widgets))
                old_focus_widget.focus_release()
                focus_widget = self.widgets[self.focus_index]
                focus_widget.focus_accept()
            # elif is_function_key(ch):
            #     self.handle_menu(ch)

    def box_form(self):
        self.stdscr.border(0,0,0,0,0,0,0)

    def make_boxes(self):
        # self.stdscr.border(0,0,0,0,0,0,0)
        self.title_win.border(0,0,0,0,0,0,curses.ACS_LTEE, curses.ACS_RTEE)
        self.body_win.border(0,0," "," ", curses.ACS_VLINE, curses.ACS_VLINE,0,0)
        self.menu_win.border(0,0,0,0, curses.ACS_LTEE, curses.ACS_RTEE, curses.ACS_LTEE, curses.ACS_RTEE)
        self.msg_win.border(0,0,0,0, curses.ACS_LTEE, curses.ACS_RTEE, 0, 0)


    def render_message(self):
        return
        self.msg_win.addstr(1,1, " Msg: ", Colors.msg_label_attr())

    def render(self):
        self.make_boxes()
        self.title_win.addstr(2, (self.width // 2) - (len(self.title) // 2), self.title, Colors.title_attr())
        self.title_win.noutrefresh()
        self.body_win.noutrefresh()
        self.menu_win.noutrefresh()
        self.msg_win.noutrefresh()

        for w in self.widgets:
            w.render()

        self.render_message()

        curses.doupdate()
        # self.stdscr.refresh()

    def run(self):
        self.widgets[self.focus_index].focus_accept()
        self.render()
        while True:
            self.render()
            self.handle_input()

    def get_values(self):
        result = {}
        ok = True
        for w in self.widgets:
            # b1 = hasattr (w, "validator") 
            # b2 = hasattr(w, "id") 
            # b3 = hasattr(w, "get_value") 
            # b4 = callable(getattr(w.__class__, "get_value"))
            if hasattr(w, "validator") and hasattr(w, "id") and hasattr(w, "get_value") and callable(getattr(w, "get_value")) :
                v = w.get_value()
                tmp = w.validator.validate(v) 
                if tmp is not None:
                    result[w.id] = tmp
                    ok = ok and True
                else:
                    ok = ok and False
                    self.msg_error(w.validator.error_message())    

        return result if ok else None


from turtle import right
from typing import List
import curses
import curses.textpad

from simple_curses.colors import Colors
import simple_curses.menu as M
from simple_curses.message_widget import MessageWidget
from widget_base import WidgetBase


def is_next_control(ch):
    return ch == "KEY_RIGHT" or ch == curses.KEY_RIGHT


def is_prev_control(ch):
    return ch == "KEY_LEFT" or ch == curses.KEY_LEFT


def is_function_key(ch):
    tmp = ch[0:6]
    return tmp == "KEY_F("


def fn_key_match(k1, k2):
    return k1 == k2


def fn_key_description(k1):
    s1 = k1.replace("KEY_F(", "")
    s2 = s1.replace(")", "")
    s3 = "F" + s2
    return s3

class Rectangle:
    def __init__(self, nbr_rows, nbr_cols, y_beg, x_beg ):
        self.nbr_rows = nbr_rows
        self.nbr_cols = nbr_cols
        self.y_begin = y_beg
        self.x_begin = x_beg

class VStack:
    def __init__(self, win: curses.window, widgets: List[WidgetBase]):
        
        pass
class ViewBodyLeft:
    pass

class ViewBodyRight:
    pass

class ViewBody:
    pass

class ViewMenu:
    def __init__(self, form, stdscr, menu_win: curses.window, menu_items: List[M.MenuItem]):
        self.outter_win = menu_win
        self.height, self.width = menu_win.getmaxyx()
        ybeg, xbeg = menu_win.getbegyx()
        max_item_width = 0
        total_width = 0
        item_width = None
        for m in menu_items:
            max_item_width = m.get_width() if max_item_width < m.get_width() else max_item_width
            total_width += m.get_width() + 4
        if (max_item_width + 2) * len(menu_items) < self.width:
            item_width = max_item_width + 2 
        else: 
            raise ValueError("cannot fit the menu items in a single line  with nice spacing")
        xpos = xbeg + self.width - item_width
        rectangles = []
        for m in reversed(menu_items):
            r = Rectangle(3, item_width - 2, ybeg + 1, xpos) #leave a space between the menu items
            rectangles.append(r)
            xpos += -item_width
            tmp_win = self.outter_win.subwin(r.nbr_rows, r.nbr_cols, r.y_begin, r.x_begin)
            m.set_enclosing_window(tmp_win)
            m.set_form(form)
            m.has_focus = False


class View:
    pass

class Form:
    def __init__(
        self, 
        stdscr, 
        height, 
        width, 
        left_widgets, right_widgets, menu_widgets,
        context, 
        input_timeout_ms=2
        ):
        self.height = height
        self.width = width
        self.left_widgets = left_widgets
        self.right_widgets = right_widgets
        self.menu_widgets = menu_widgets
        self.widgets = left_widgets + right_widgets + menu_widgets
        self.context = context
        self.stdscr = stdscr
        self.focus_index = 0
        self.title = "This is a data entry form"
        self.input_timeout_ms = input_timeout_ms

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

        body_start_row = self.body_start_row  # 4
        body_start_col = 0

        curses.mousemask(curses.ALL_MOUSE_EVENTS + curses.REPORT_MOUSE_POSITION)

        self.body_win = curses.newwin(self.body_height, self.width, self.body_start_row, 0)
        self.message_widget = MessageWidget(self.msg_start_row, 0, "", "", self.msg_width, self.msg_height, "", context)
        self.message_widget.set_enclosing_window(curses.newwin(self.msg_height, self.msg_width, self.msg_start_row, 0))
        self.message_widget.set_form(self)

        self.menu_win = curses.newwin(self.menu_height, self.menu_width, self.menu_start_row, 0)
        # self.msg_win.bkgd(" ", Colors.button_focus())
        self.message_text = ""
        body_height = 0
        col = body_start_col + 4
        c = 1
        self.menu_items = []
        self.non_menu_widgets = []
        for w in self.widgets:
            klass = w.__class__.__name__
            if klass == "MenuItem":
                self.menu_items.append(w)
                w.set_form(self)
                w.has_focus = False
                # # this is a horizonal stack of the menu items - would like it to be right justified
                # ymnu, xmnu = self.menu_win.getbegyx()
                # ymm, xmm = self.menu_win.getmaxyx()
                # # w.set_enclosing_window(curses.newwin(w.get_height(), w.get_width(), self.msg_start_row + 1, col + 1))
                # tmp_win = self.menu_win.subwin(3, 10, ymnu+1, xmnu + col)
                # w.set_enclosing_window(tmp_win)
                # col += w.get_width() + 4
                # c += w.get_width() + 4
            else:
                self.non_menu_widgets.append(w)
                w.set_form(self)
                w.has_focus = False

        for w in self.non_menu_widgets:
            w.start_row = w.row + body_start_row
            w.start_col = w.col + body_start_col
            w.set_enclosing_window(curses.newwin(w.get_height(), w.get_width(), self.body_start_row + w.row,
                                                    self.body_start_col + w.col))

        self.view_menu = ViewMenu(self, self.stdscr, self.menu_win, self.menu_items)

        zz = self.body_win.getparyx()
        z2 = self.title_win.getparyx()
        z3 = z2

    def msg_error(self, s: str):
        self.message_widget.msg_error(s)

    def msg_warn(self, s):
        self.message_widget.msg_warn(s)

    def msg_info(self, s):
        self.message_widget.msg_info(s)

    def shift_focus_to(self, w_index):
        old_focus_widget = self.widgets[self.focus_index]
        self.focus_index = w_index
        old_focus_widget.focus_release()
        focus_widget = self.widgets[self.focus_index]
        focus_widget.focus_accept()

    def mouse_in_widget(self, w, y, x):
        """Tests whether the mouse position y,x is inside the widget w"""
        return w.rectangle().contains(y, x)

    def handle_input(self):
        # enable getch wait 
        self.stdscr.timeout(-1)
        n = 0
        while True:
            ch = self.stdscr.getch()
            if ch == curses.ERR:
                break;
            if ch == curses.KEY_MOUSE:
                dev_id, y, x, z, buttonevent = curses.getmouse()
                self.message_widget.msg_info(
                    "handle_input.mouse event id:{} y:{} x:{} button:{}".format(dev_id, y, x, z, hex(buttonevent)))
                # for w in self.widgets:
                #     if self.mouse_in_widget(w, y, x):
                #         pass

            self.stdscr.timeout(100)

            n += 1
            chstr = chr(ch) if ch <= 255 else hex(ch)
            if chstr in ['\n', '\r', '\t']:
                chstr = "??"
            self.message_widget.msg_info("handle_input ch: {} hex: {}".format(chstr, hex(ch)))
            focus_widget = self.widgets[self.focus_index]
            focus_widget.focus_accept()
            if focus_widget.handle_input(ch):
                continue
            else:
                if is_next_control(ch):
                    w_index = (self.focus_index + 1 + len(self.widgets)) % (len(self.widgets))
                    self.shift_focus_to(w_index)
                elif is_prev_control(ch):
                    w_index = (self.focus_index - 1 + len(self.widgets)) % (len(self.widgets))
                    self.shift_focus_to(w_index)
                # elif is_function_key(ch):
                #     self.handle_menu(ch)

    def box_form(self):
        self.stdscr.border(0, 0, 0, 0, 0, 0, 0)

    def make_boxes(self):
        self.title_win.border(0, 0, 0, 0, 0, 0, curses.ACS_LTEE, curses.ACS_RTEE)
        self.body_win.border(0, 0, " ", " ", curses.ACS_VLINE, curses.ACS_VLINE, 0, 0)
        self.menu_win.border(0, 0, 0, 0, curses.ACS_LTEE, curses.ACS_RTEE, curses.ACS_LTEE, curses.ACS_RTEE)

    def render(self):
        self.make_boxes()
        self.title_win.addstr(2, (self.width // 2) - (len(self.title) // 2), self.title, Colors.title_attr())
        self.title_win.noutrefresh()
        self.body_win.noutrefresh()
        self.menu_win.noutrefresh()

        for w in self.widgets:
            w.render()
        self.message_widget.render()

        curses.doupdate()
        # self.stdscr.refresh()

    def run(self):
        self.widgets[self.focus_index].focus_accept()
        self.render()
        while True:
            self.handle_input()
            self.render()

    def get_values(self):
        result = {}
        ok = True
        for w in self.widgets:
            # b1 = hasattr (w, "validator") 
            # b2 = hasattr(w, "id") 
            # b3 = hasattr(w, "get_value") 
            # b4 = callable(getattr(w.__class__, "get_value"))
            if hasattr(w, "validator") and hasattr(w, "id") and hasattr(w, "get_value") and callable(
                    getattr(w, "get_value")):
                v = w.get_value()
                tmp = w.validator.validate(v)
                if tmp is not None:
                    result[w.id] = tmp
                    ok = ok and True
                else:
                    ok = ok and False
                    self.message_widget.msg_error(w.validator.error_message())

        return result if ok else None

from typing import List
import curses
import curses.textpad

from simple_curses.message_widget import MessageWidget
from simple_curses.keyboard import is_control_v
from simple_curses.colors import Colors
from simple_curses.theme import Theme
from simple_curses.keyboard import is_next_control, is_prev_control

# def is_next_control(ch):
#     return ch == "KEY_RIGHT" or ch == curses.KEY_RIGHT


# def is_prev_control(ch):
#     return ch == "KEY_LEFT" or ch == curses.KEY_LEFT


# def is_function_key(ch):
#     tmp = ch[0:6]
#     return tmp == "KEY_F("


# def fn_key_match(k1, k2):
#     return k1 == k2


# def fn_key_description(k1):
#     s1 = k1.replace("KEY_F(", "")
#     s2 = s1.replace(")", "")
#     s3 = "F" + s2
#     return s3


class AppBase:
    def __init__(self, stdscr, body_height, width, context, input_timeout_ms=2):
        self.theme = Theme.instance()
        self.width = width
        self.views = None
        self.data = None
        self.log_keystrokes = True
        self.context = context
        self.stdscr = stdscr
        self.focus_index = 0
        self.focus_widgets = []
        self.top_menu_items = []
        self.render_widgets = []
        self.title = "This is a data entry form"
        self.input_timeout_ms = input_timeout_ms

        # self.menu_height = 5
        self.msg_height = 20
        self.title_height = 5
        self.body_height = body_height
        self.height = self.body_height + self.title_height + self.msg_height + 2

        self.outter_win = curses.newwin(self.height + 2, self.width + 2, 0, 0)
        y_outter, x_outter = self.outter_win.getbegyx()
        y_outter_m, x_outter_m = self.outter_win.getmaxyx()
        self.title_win = curses.newwin(self.title_height, self.width, y_outter, 0)

        curses.mousemask(curses.ALL_MOUSE_EVENTS + curses.REPORT_MOUSE_POSITION)

        self.body_win = curses.newwin(self.body_height, self.width, y_outter + self.title_height, 0)
        # self.body_win.bkgd(" ", Colors.button_focus())
        ybdy, xbdy = self.body_win.getbegyx()
        ybdym, xbdym = self.body_win.getmaxyx()
        self.message_widget = MessageWidget(self, ybdy + ybdym - 1, 0, "", "", self.width, self.msg_height, "", context)
        msg_win = curses.newwin(self.msg_height, self.width, ybdy + ybdym - 1, 0)
        self.message_widget.set_enclosing_window(msg_win)
        # self.message_widget.set_form(self)
        # ymsg, xmsg = msg_win.getbegyx()
        # ymsgm, xmsgm = msg_win.getmaxyx()
        self.register_views()
        self.current_view_index = 0
        self.show_current_view()

    def register_views(self):
        # this method should be overridden by a derived class when buildign an actual app
        raise NotImplementedError()

    def get_current_view(self):
        return self.views[self.current_view_index]

    def show_current_view(self):
        self.views[self.current_view_index].show()
        self.focus_widgets = self.top_menu_items + self.views[self.current_view_index].get_focus_widgets()
        self.render_widgets = self.top_menu_items + self.views[self.current_view_index].get_render_widgets() + [
            self.message_widget]

    def hide_current_view(self):
        self.views[self.current_view_index].hide()

    def change_view(self, next_view):
        self.views[self.current_view_index].hide()
        self.current_view_index = next_view % len(self.views)
        self.focus_index = 0
        self.views[self.current_view_index].show()
        self.focus_widgets = self.top_menu_items + self.views[self.current_view_index].get_focus_widgets()
        self.render_widgets = self.top_menu_items + self.views[self.current_view_index].get_render_widgets() + [
            self.message_widget]

    def next_view(self):
        self.views[self.current_view_index].hide()
        self.current_view_index = (self.current_view_index + 1) % len(self.views)
        self.focus_index = 0
        self.views[self.current_view_index].show()
        self.focus_widgets = self.top_menu_items + self.views[self.current_view_index].get_focus_widgets()
        self.render_widgets = self.top_menu_items + self.views[self.current_view_index].get_render_widgets() + [
            self.message_widget]

    def enable(self):
        pass

    def disable(self):
        pass

    def msg_error(self, s):
        self.message_widget.msg_error(s)

    def msg_warn(self, s):
        self.message_widget.msg_warn(s)

    def msg_info(self, s):
        self.message_widget.msg_info(s)

    def shift_focus_to(self, w_index):
        old_focus_widget = self.focus_widgets[self.focus_index]
        self.focus_index = w_index
        old_focus_widget.focus_release()
        focus_widget = self.focus_widgets[self.focus_index]
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
                break
            if ch == curses.KEY_MOUSE:
                dev_id, y, x, z, buttonevent = curses.getmouse()
                self.message_widget.msg_info(
                    "handle_input.mouse event id:{} y:{} x:{} z:{} button:{}".format(dev_id, y, x, z, hex(buttonevent)))

            self.stdscr.timeout(100)

            n += 1
            chstr = chr(ch) if ch <= 255 else hex(ch)
            if chstr in ['\n', '\r', '\t']:
                chstr = "??"
            if self.log_keystrokes:    
                self.message_widget.msg_info("handle_input ch: {} hex: {}".format(chstr, hex(ch)))

            focus_widget = self.focus_widgets[self.focus_index]
            focus_widget.focus_accept()
            
            if focus_widget.handle_input(ch):
                continue
            else:
                if is_next_control(ch):
                    w_index = (self.focus_index + 1 + len(self.focus_widgets)) % (len(self.focus_widgets))
                    self.shift_focus_to(w_index)
                elif is_prev_control(ch):
                    w_index = (self.focus_index - 1 + len(self.focus_widgets)) % (len(self.focus_widgets))
                    self.shift_focus_to(w_index)
                elif is_control_v(ch):
                    self.next_view()
                # elif is_function_key(ch):
                #     self.handle_menu(ch)

    def box_form(self):
        self.stdscr.bkgd(" ", Colors.black_white())
        self.stdscr.border(0, 0, 0, 0, 0, 0, 0)

    def make_boxes(self):
        # a1 = Colors.black_white()
        # a11 = Colors.white_black()
        # a2 = Theme.bkgd_attr()
        # raise RuntimeError()
        self.title_win.bkgd(" ", Theme.instance().bkgd_attr());
        self.title_win.border(0, 0, 0, 0, 0, 0, curses.ACS_LTEE, curses.ACS_RTEE)
        self.body_win.bkgd(" ", Theme.instance().bkgd_attr());
        self.body_win.border(0, 0, " ", " ", curses.ACS_VLINE, curses.ACS_VLINE, 0, 0)

    def render(self):
        self.make_boxes()
        self.title_win.noutrefresh()
        self.body_win.noutrefresh()

        # for w in self.render_widgets:
        #     w.render()

        self.views[self.current_view_index].render()
        self.message_widget.render()

        curses.doupdate()

    def run(self):
        self.focus_widgets[self.focus_index].focus_accept()
        self.render()
        while True:
            self.handle_input()
            self.render()

    def get_values(self):
        result = {}
        ok = True
        for w in self.focus_widgets:
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

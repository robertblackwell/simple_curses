from typing import List
import curses
import curses.textpad
from time import sleep

from simple_curses.message_widget import MessageWidget
from simple_curses.keyboard import is_control_v
from simple_curses.colors import Colors
from simple_curses.theme import Theme
from simple_curses.keyboard import is_next_control, is_prev_control
import simple_curses.window as Window
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

def min_size_for_views(views):
    h = 0
    w = 0
    for v in views:
        h = v.get_height() if v.get_height() > h else h
        w = v.get_width() if v.get_width() > w else w
    return (h, w)

def test_screen_size(stdscr, height, width):
    h, w = stdscr.getmaxyx()
    pair = curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    color = curses.color_pair(1) + curses.A_BOLD
    while h < height or w < width:
    
        stdscr.addstr(0, 0, "                              ")
        stdscr.addstr(1, 0, "                                                                     " )
        stdscr.addstr(2, 0, "                                                                     ")
        stdscr.refresh()
        sleep(.3)
        stdscr.addstr(0, 0, "The screen window is too small", color)
        stdscr.addstr(1, 0, "Must be at least {} high and {} wide currently is high: {} wide: {}".format(height, width, h, w), color)
        stdscr.addstr(2, 0, "To quit hit Cntrl C/Z otherwise enlarge the screen and hit y/Y+Return", color)
        stdscr.refresh()
        ch = " "
        while not(ch == ord('y') or ch == ord('Y')):
            ch = stdscr.getch()
            char = chr(ch)
        h, w = stdscr.getmaxyx()


class AppBase:
    def __init__(self, stdscr, body_height, width, msg_height=10, context=None, input_timeout_ms=2):
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
        self.register_views()

        # Now calculate the size of the full display of the app
        self.body_height, self.body_width = min_size_for_views(self.views)
        self.width = 1 + self.body_width + 1 #allow for border on both sides 
        self.msg_height = msg_height
        self.top_menu_height = 5
        
        #allow for top and bottom border plus horizontal lines after the top menu and after the body
        self.height = 1 + self.top_menu_height + 1 + self.body_height + 1 + self.msg_height + 1
        test_screen_size(stdscr, self.height, self.width)
        # Create an outter window that will have all content inside it
        self.outter_win = curses.newwin(self.height, self.width, 0, 0)

        #create a vertical stack of windows inside outter window. These will be the 'frame' for the application
        mark_territory = False
        self.top_menu_win  = Window.newwin_inside(self.outter_win, self.top_menu_height, self.body_width, 1, 1)
        if mark_territory:
            self.top_menu_win.bkgd("1")
            self.top_menu_win.refresh()
        self.top_hline_win = Window.hline_after(self.top_menu_win)
        self.body_win      = Window.newwin_after(self.top_hline_win, self.body_height, self.body_width, 1)
        if mark_territory:
            self.body_win.bkgd("2")
            self.body_win.refresh()
        self.bottom_hline  = Window.hline_after(self.body_win)
        self.msg_win       = Window.newwin_after(self.bottom_hline, self.msg_height, self.body_width, 1)
        if mark_territory:
            self.msg_win.bkgd("3")
            self.msg_win.refresh()


        self.message_widget = MessageWidget(self, "msg_01", "Message Box", self.body_width, self.msg_height, "", context)

        #connect the widgets to their enclosing windows
        for v in self.views:
            v.set_enclosing_window(self.body_win)

        self.message_widget.set_enclosing_window(self.msg_win)
        self.current_view_index = 0
        self.show_current_view()

    def register_views(self):
        """
        this method should be overridden by a derived class when buildign an actual app
        should set self.views
        """


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

    def render_frame(self):
        self.outter_win.box()
        Window.draw_hline(self.top_hline_win)
        Window.draw_hline(self.bottom_hline)

    def render_contents(self):
        self.views[self.current_view_index].render()
        self.message_widget.render()
        return
        self.top_menu_win.bkgd(" ", curses.color_pair(2))
        self.top_menu_win.addstr(0, 0, "This is top menu", curses.A_BOLD)
        self.body_win.bkgd(" ", curses.color_pair(2))
        self.body_win.addstr(0, 0, "This is body win", curses.A_BOLD)
        self.msg_win.bkgd(" ", curses.color_pair(2))
        self.msg_win.addstr(0, 0, "This is msgwin", curses.A_BOLD)

    def noutrefresh_frame(self):    
        self.stdscr.noutrefresh()
        self.outter_win.noutrefresh()
        self.top_menu_win.noutrefresh()
        self.top_hline_win.noutrefresh()
        self.body_win.noutrefresh()
        self.bottom_hline.noutrefresh()
        self.msg_win.noutrefresh()


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
        self.render_frame()
        self.noutrefresh_frame()
        self.render_contents()
        curses.doupdate()
        return
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

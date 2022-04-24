import curses
import curses.textpad
import textwrap
from abc import ABC
from .colors import Colors
from .widget_base import WidgetBase
from simple_curses.theme import Theme

class MessageWidget(WidgetBase, ABC):
    """This widget provides a box into which messsages can be written.
    Each message is a single line.
    -   The message is truncated to fit into a line or contoinued onto the next line
    -   The messages are visible through a view window
    -   Only the last N messages are visible
    -   The most recent message is at the bottom
    -   The widget is enclosed by a box
    -   The row, col, height, width args to the constructor are the position and size of the enclosing box
    -   The message area starts at row+1, col+1 and has size height-2 width-2 
    """

    @classmethod
    def classmeth(cls):
        pass

    def __init__(self, app, key, label, width, height, attributes, data):
        self.app = app
        self.content_win = None
        self.win = None
        self.key = key
        self.label = label
        self.width = width
        self.height = height
        self.data = data
        self.messages = []
        self.msg_count = 0
        self.has_focus = False

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def focus_accept(self):
        pass

    def focus_release(self):
        pass

    def set_enclosing_window(self, win):
        self.win = win
        h, w = self.win.getmaxyx()
        r, c = self.win.getbegyx()
        r_sub = r + 1
        c_sub = c + 1
        h_sub = h - 2
        w_sub = w - 2
        # self.content_win = self.win.subwin(h_sub, w_sub, r_sub, c_sub)
        pass

    def msg_error(self, msg):
        label = " ERROR: "
        self.msg_post(label, msg, Theme.instance().msg_error_attr())

    def msg_warn(self, msg):
        label = " WARNING: "
        self.msg_post(label, msg, Theme.instance().msg_warn_attr())

    def msg_info(self, msg):
        label = " INFO: "
        self.msg_post(label, msg, Theme.instance().msg_info_attr())

    def msg_post(self, label, msg, attr):
        self.msg_count += 1
        if len(msg) > self.width - 20:
            msg_lines = textwrap.wrap(msg, self.width - 20)
            lnindex = 0
            for ln in msg_lines:
                if lnindex == 0:
                    self.messages.append([self.msg_count, label, ln, attr])
                else:
                    self.msg_count += 1
                    self.messages.append([self.msg_count, "     CONT: ", ln, attr])
                
                lnindex += 1
        else:
            self.messages.append([self.msg_count, label, msg, attr])

    def handle_input(self, chint):
        return False

    def render(self):
        self.win.clear()
        self.win.bkgd(" ", Theme.instance().bkgd_attr())
        # self.win.attron(Theme.instance().cursor_attr())
        # self.win.border(0, 0, 0, 0, curses.ACS_LTEE, curses.ACS_RTEE, 0, 0)
        # self.win.attron(Theme.instance().label_attr(False))
        lenmsgs = len(self.messages)
        if lenmsgs <= self.height:
            active_messages = self.messages
        else:
            k = lenmsgs - self.height
            active_messages = self.messages[k: lenmsgs]

        r = 1
        for msg in active_messages:
            astring = " {0:>3}:{1}{2}".format(msg[0], msg[1], msg[2])
            if len(astring) > self.width - 10:
                astring = astring[0:self.width - 10]+".."
            else:
                astring.ljust(self.width - 10)
            self.win.addstr(r - 1, 0, astring, msg[3])
            r += 1

        self.win.noutrefresh()
        curses.doupdate()

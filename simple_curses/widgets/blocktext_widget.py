import curses
from typing import List, Union, Any

from simple_curses.widget_base import WidgetBase, FocusableWidgetBase
from simple_curses.kurses_ex import make_subwin, win_addstr
from simple_curses.theme import Theme
import simple_curses.version as V

banner_lines_01 = [
    "**********************************************************************************",
    "*              ****************************************************              *",
    "*              *                      AORC                        *              *",
    "*              *                                                  *              *",
    "*              *                                                  *              *",
    "*              *    For issues with this script, please reach     *              *",
    "*              *              out to Fred TheCoder                *              *",
    "*              *                                                  *              *",
    "*              *             fred@the_coder.io                    *              *",
    "*              *             simple_curses v{}              *              *".format(V.__version__),
    "*              *             fred@the_coder.io                    *              *",
    "*              ****************************************************              *",
    "*                                                                                *",
    "**********************************************************************************",
]

help_lines = [
    "**********************************************************************************",
    "*  Help for simple_curses app                                                     *",
    "*           Have not written it yet                                               *",
    "**********************************************************************************",
]


class BlockTextWidget(WidgetBase):
    """A widget that displays a multi line block of text"""
    def __init__(self, app, text_block: List[str]):
        self.height = len(text_block)
        self.width = 0
        for line in text_block:
            self.width = len(line) if len(line) > self.width else self.width
        self.text_block = text_block
        self.app = app
        self.parent_view = None
        self.outter_win = None
        self.banner_win = None
        self.has_focus = False

    def set_enclosing_window(self, window):
        self.outter_win = window
        ybeg, xbeg = window.getbegyx()
        ym, xm = window.getmaxyx()
        if ym < self.height:
            raise ValueError("ym: {} is too small, required {}".format(ym, self.height))
        if xm < self.width:
            raise ValueError("xm: {} is too small, required {}".format(xm, self.width))
        rbeg = 0  # ((ym - self.height) // 2)
        cbeg = 0  # ((xm - self.width) // 2)
        # self.banner_win = make_subwin(window, self.height+1, self.width+1, rbeg, cbeg)
        self.banner_win = make_subwin(window, self.height, self.width, rbeg, cbeg)

    def render(self):
        if self.banner_win is None:
            raise RuntimeError("banner_win is none")
        self.banner_win.bkgd(" ", Theme.instance().label_attr(self.has_focus))
        r = 0
        for line in self.text_block:
            ln = len(line)
            ym, xm = self.banner_win.getmaxyx()

            # NOTE:Hack to fix a bug in curses module 
            # the curses.win.addstr function will not allow writing the very last position in a win
            # the fix is in kurses_ex.win_addstr
            if True:
                win_addstr(self.banner_win, r, 0, line, Theme.instance().label_attr(self.has_focus))
            else:
                self.banner_win.addstr(r, 0, line[0:xm-1], Theme.instance().label_attr(self.has_focus))

            r += 1

        self.banner_win.noutrefresh()

    def handle_input(self, ch):
        return False

class HelpWidget(BlockTextWidget):
    def __init__(self, app):
        super().__init__(app, help_lines)

class BannerWidget(BlockTextWidget):
    def __init__(self, app):
        super().__init__(app, banner_lines_01)


# class HelpWidget(BlockTextWidget):
#     def __init__(self, app):
#         super().__init__(app, help_lines)

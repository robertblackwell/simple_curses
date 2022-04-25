import curses
from typing import List, Union, Any

from simple_curses.widget_base import WidgetBase
from simple_curses.kurses_ex import make_subwin
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
    "*  Lumen application TEST                                                        *",
    "*              ****************************************************              *",
    "*              *                      Lumen                       *              *",
    "*              *                     Security                     *              *",
    "*              *                                                  *              *",
    "*              *      DDoS 2.0 Always On Prefix List Script       *              *",
    "*              *                                                  *              *",
    "*              *    For issues with this script, please reach     *              *",
    "*              *              out to Richard Blackwell            *              *",
    "*              *                                                  *              *",
    "*              *            richardr.blackwell@lumen.com          *              *",
    "*              *               DL-SPIDDOSWAF@lumen.com            *              *",
    "*              ****************************************************              *",
    "*                                                                                 *",
    "**********************************************************************************",
]


class BlockTextWidget(WidgetBase):
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

    def focus_accept(self):
        self.has_focus = True

    def focus_release(self):
        self.has_focus = False

    def get_height(self):
        return self.height  # +1# + 2

    def get_width(self):
        return self.width + 1  # + 2

    def set_parent_view(self, view):
        self.parent_view = view

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
        self.banner_win = make_subwin(window, self.height, self.width + 1, rbeg, cbeg)

    # def set_app(self, app):
    #     self.app = app

    def render(self):
        if self.banner_win is None:
            raise RuntimeError("banner_win is none")
        self.banner_win.bkgd(" ", Theme.instance().label_attr(self.has_focus))
        r = 0
        for line in self.text_block:
            ln = len(line)
            ym, xm = self.banner_win.getmaxyx()
            self.banner_win.addstr(r, 0, line[0:xm-1], Theme.instance().cursor_attr())
            r += 1

        self.banner_win.noutrefresh()

    def handle_input(self, ch):
        return False


class BannerWidget(BlockTextWidget):
    def __init__(self, app):
        super().__init__(app, banner_lines_01)


class HelpWidget(BlockTextWidget):
    def __init__(self, app):
        super().__init__(app, help_lines)

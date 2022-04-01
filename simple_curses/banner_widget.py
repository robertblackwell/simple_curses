import curses
from typing import List
from simple_curses import *

# from widget_base import WidgetBase
# from kurses_ex import make_subwin
# from colors import Colors

banner_lines_01 = [
    "**********************************************************************************",
    "*                       _                                                        *",
    "*                      | |                                                       *",
    "*                      | |    _   _ _ __ ___   ___ _ __                          *",
    "*                      | |   | | | | '_ ` _ \ / _ \ '_ \                         *",
    "*                      | |___| |_| | | | | | |  __/ | | |                        *",
    "*                      \_____/\__,_|_| |_| |_|\___|_| |_|                        *",
    "*              ****************************************************              *",
    "*              *                      Lumen                       *              *",
    "*              *                     Security                     *              *",
    "*              *                                                  *              *",
    "*              *      DDoS 2.0 Always On Prefix List Script       *              *",
    "*              *                                                  *              *",
    "*              *    For issues with this script, please reach     *              *",
    "*              *              out to Chris Jensen                 *              *",
    "*              *                                                  *              *",
    "*              *             jensen.christian@lumen.com           *              *",
    "*              *               DL-SPIDDOSWAF@lumen.com            *              *",
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
        self.width = len(text_block[0])
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

    def set_enclosing_window(self, window: curses.window):
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
        if self.has_focus:
            self.banner_win.bkgd(" ", Colors.green_black())
        else:
            self.banner_win.bkgd(" ", Colors.white_black())
        r = 0
        for line in self.text_block:
            ln = len(line)
            ym, xm = self.banner_win.getmaxyx()
            self.banner_win.addstr(r, 0, line)
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

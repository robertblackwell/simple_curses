import curses
from typing import List
from widget_base import WidgetBase
from view import View
from kurses_ex import make_subwin

banner_lines = [
"**********************************************************************************",
"                        _                                                         ",
"                       | |                                                        ",
"                       | |    _   _ _ __ ___   ___ _ __                           ",
"                       | |   | | | | '_ ` _ \ / _ \ '_ \                          ",
"                       | |___| |_| | | | | | |  __/ | | |                         ",
"                       \_____/\__,_|_| |_| |_|\___|_| |_|                         ",
"               ****************************************************               ",
"               *                      Lumen                       *               ",
"               *                     Security                     *               ",
"               *                                                  *               ",
"               *      DDoS 2.0 Always On Prefix List Script       *               ",
"               *                                                  *               ",
"               *                                                  *               ",
"               *                                                  *               ",
"               *    For issues with this script, please reach     *               ",
"               *              out to Chris Jensen                 *               ",
"               *                                                  *               ",
"               *             jensen.christian@lumen.com           *               ",
"               *               DL-SPIDDOSWAF@lumen.com            *               ",
"               ****************************************************               ",
"                                                                                  ",
"**********************************************************************************",
]
class BannerWidget(WidgetBase):
    def __init__(self):
        self.height = len(banner_lines)
        self.width = len(banner_lines[0])
        self.form = None
        self.outter_win = None
        pass
    
    def get_height(self):
        return self.handle_input

    def get_width(self):
        return self.width

    def set_enclosing_window(self, window: curses.window):
        self.outter_win = window
        ybeg, xbeg = window.getbegyx()
        ym, xm = window.getmaxyx()
        if ym < self.height:
            raise ValueError("ym: {} is too small, required {}".format(ym, self.height))
        if xm < self.width:
            raise ValueError("xm: {} is too small, required {}".format(xm, self.width))
        rbeg = ((ym - self.height) // 2) - 1
        cbeg = ((xm - self.width) // 2) - 1
        self.banner_win = make_subwin(window, self.height, self.width, rbeg, cbeg)

    def set_form(self, form):
        self.form = form

    def render(self):
        for line in banner_lines:
            self.banner_win.addstr(0, 0, line)
        self.banner_win.noutrefresh()


class BannerView(View):

        def __init__(self, ident: str, label: str, form, stdscr, window: curses.window, widgets: List[WidgetBase], menu_items: List[M.MenuItem]):



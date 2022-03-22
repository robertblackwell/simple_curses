from typing import List
import curses
import curses.textpad
from kurses_ex import make_subwin

import simple_curses.menu as M
from widget_base import WidgetBase
from layout import ColumnLayout, Rectangle


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


class ViewBody:

    def __init__(self, form, stdscr, win: curses.window, widgets: List[WidgetBase]):
        self.outter_win = win
        yh, xw = win.getmaxyx()
        ybeg, xbeg = win.getbegyx()
        require_borders = True
        if require_borders:
            self.height = yh - 2
            self.width = xw - 2
            ybeg = ybeg + 1
            xbeg = xbeg + 1

        max_widget_width = 0
        total_width = 0
        item_width = None
        widgets_total_height = 0
        # calculate the widests widget and the total height required with 1 row between
        for w in widgets:
            max_widget_width = w.get_width() if max_widget_width < w.get_width() else max_widget_width
            total_width += w.get_width() + 4
            widgets_total_height += w.get_height() + 1

        # how many columns that wide could we make - leaving 2 spaces on each side of a widget
        max_columns = self.width // (max_widget_width + 1)

        required_columns = (widgets_total_height // self.height) if (widgets_total_height % self.height) == 0 else (
                                                                                                                               widgets_total_height // self.height) + 1

        if required_columns > max_columns:
            raise ValueError("cannot fit {}  widgets in window of size y: {} x:{}".format(len(widgets), yh, xw))

        self.nbr_columns = required_columns

        nbr_widgets_per_column = len(widgets) // required_columns

        nbr_columns_with_one_extra = len(widgets) % required_columns

        clayout = ColumnLayout(self.height, max_widget_width)
        clayout.add_widgets(widgets)
        self.widget_allocation = clayout.widget_allocation


class TopMenu:
    """This is a Horizontal Stack, LEFT justified, of menu items. Used for a Form top menu
    to switch views
    """

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
        for m in menu_items:
            r = Rectangle(3, item_width - 2, ybeg + 1, xpos)  # leave a space between the menu items
            rectangles.append(r)
            xpos += item_width
            tmp_win = self.outter_win.subwin(r.nbr_rows, r.nbr_cols, r.y_begin, r.x_begin)
            m.set_enclosing_window(tmp_win)
            m.set_form(form)
            m.has_focus = False


class ViewMenu:
    """This is a Horizontal Stack, right justified, of menu items. Used to provide a menu inside a view
    """

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
            r = Rectangle(3, item_width - 2, ybeg + 1, xpos)  # leave a space between the menu items
            rectangles.append(r)
            xpos += -item_width
            tmp_win = self.outter_win.subwin(r.nbr_rows, r.nbr_cols, r.y_begin, r.x_begin)
            m.set_enclosing_window(tmp_win)
            # m.set_form(form)
            m.has_focus = False


class BannerView:
    """A class that implements a view that dispays a single banner or info widget in the middle of the Form body. """

    def __init__(self, app, ident: str, label: str, stdscr, window: curses.window, widget: WidgetBase):
        # the outter_win will contain all the dataentry fields and across the bottom the view menu
        self.outter_win = window
        self.stdscr = stdscr
        self.height, self.width = window.getmaxyx()
        ym, xm = window.getmaxyx()
        yb, xb = window.getbegyx()
        self.outter_y_begin, self.outter_x_begin = window.getbegyx()
        self.widget = widget
        self.label = label
        self.ident = ident
        self.app = app

    def setup(self):
        w = self.widget
        ym, xm = self.outter_win.getmaxyx()
        yb, xb = self.outter_win.getbegyx()

        rbeg = (ym - w.get_height()) // 2 - 1
        if rbeg < 0:
            rbeg = 0
        cbeg = (xm - w.get_width()) // 2 - 1
        if cbeg < 0:
            cbeg = 0

        w.set_enclosing_window(self.outter_win.subwin(
            w.get_height() + 1,
            w.get_width() + 1,
            yb + rbeg,
            xb + cbeg))

    def show(self):
        self.setup()

    def hide(self):
        self.outter_win.clear()
        pass

    def get_focus_widgets(self):
        return [self.widget]

    def get_render_widgets(self):
        return [self.widget]


class View:
    """A class that implements the detailed layout and function of a Form body. A single form typically has a number of views
    that are swapped by the top menu"""

    def __init__(self, app, ident: str, label: str, stdscr, window: curses.window, widgets: List[WidgetBase],
                 menu_items: List[M.MenuItem]):
        # the outter_win will contain all the dataentry fields and across the bottom the view menu
        self.view_menu = None
        self.view_body = None
        self.menu_win = None
        self.data_entry_win = None
        self.data_entry_height = None
        self.menu_height = None
        self.outter_win = window
        self.stdscr = stdscr
        self.height, self.width = window.getmaxyx()
        ym, xm = window.getmaxyx()
        yb, xb = window.getbegyx()
        self.outter_y_begin, self.outter_x_begin = window.getbegyx()
        self.widgets = widgets
        self.menu_items = menu_items
        self.label = label
        self.ident = ident
        self.app = app

    def setup(self):
        self.menu_height = 5
        self.data_entry_height = self.height - self.menu_height  # - self.title_height - self.msg_height + 2
        body_start_col = 0
        self.data_entry_win = curses.newwin(self.data_entry_height, self.width, self.outter_y_begin + 1, 0)
        self.menu_win = curses.newwin(self.menu_height, self.width, self.outter_y_begin + self.data_entry_height, 0)
        # self.msg_win.bkgd(" ", Colors.button_focus())
        body_height = 0
        col = body_start_col + 4
        c = 1

        self.view_body = ViewBody(self, self.stdscr, self.data_entry_win, self.widgets)
        yb, xb = self.data_entry_win.getbegyx()
        for cols in self.view_body.widget_allocation.widget_columns:
            for wlo in cols.widget_layouts:
                w = wlo.widget
                x_begin = wlo.x_begin + xb
                y_begin = wlo.y_begin + yb
                sw = make_subwin(self.data_entry_win, w.get_height(), w.get_width(), wlo.y_begin, wlo.x_begin)
                w.set_enclosing_window(sw)

        self.view_menu = ViewMenu(self, self.stdscr, self.menu_win, self.menu_items)

    def get_values(self):
        v = []
        for w in self.widgets:
            v.append(w.get_value())

    def show(self):
        self.setup()

    def hide(self):
        self.outter_win.clear()

    def get_focus_widgets(self):
        return self.widgets + self.menu_items

    def get_render_widgets(self):
        return self.widgets + self.menu_items


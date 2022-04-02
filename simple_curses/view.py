from typing import List, Tuple, Dict, Any, cast
import curses
import curses.textpad

# import simple_curses.menu as M
from simple_curses.widget_base import EditableWidgetBase, WidgetBase, MenuItem, is_editable, is_focusable
from simple_curses.layout import Rectangle, ColumnLayout
from simple_curses.validator import *
from simple_curses.title_widget import TitleWidget
from simple_curses.menu import *
from simple_curses.kurses_ex import make_subwin

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

    def render(self):
        self.widget.render()



class TopMenu:
    """This is a Horizontal Stack, LEFT justified, of menu items. Used for a Form top menu
    to switch views
    """

    def __init__(self, form, stdscr, menu_win: curses.window, menu_items: List[MenuItem]):
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
            m.has_focus = False


class ViewMenu:
    """This is a Horizontal Stack, right justified, of menu items. Used to provide a menu inside a view
    """

    def __init__(self, app, parent_view, stdscr, menu_win: curses.window, menu_items: List[MenuItem]):
        self.app = app
        self.parent_view = parent_view
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
            m.has_focus = False

       
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

        required_columns = (widgets_total_height // self.height) if (widgets_total_height % self.height) == 0 else (widgets_total_height // self.height) + 1

        if required_columns > max_columns:
            raise ValueError("cannot fit {}  widgets in window of size y: {} x:{}".format(len(widgets), yh, xw))

        self.nbr_columns = required_columns

        nbr_widgets_per_column = len(widgets) // required_columns

        nbr_columns_with_one_extra = len(widgets) % required_columns

        clayout = ColumnLayout(self.height, max_widget_width)
        clayout.add_widgets(widgets)
        self.widget_allocation = clayout.widget_allocation



class View:
    """A class that implements the detailed layout and function of a data entry view body body. A single app typically has a number of views
    that are swapped by the top menu or keyboard short cuts. This class represents the type of view that has data entry fields
    and an action menu at the bottom.
    
    This view and its companions ViewMenu and ViewBody perform the layout calculations

    """

    def __init__(self, app, ident: str, title: str, stdscr, window: curses.window, widgets: List[WidgetBase],
                 menu_items: List[MenuItem]):
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
        self.focus_widgets = [w for w in (self.widgets + cast("List[WidgetBase]", self.menu_items)) if is_focusable(w) ]
        # for w in (self.menu_items + self.widgets):
        #     klass = w.__class__
        #     bases = klass.__bases__
        #     if is_focusable(w):
        #     # if isinstance(w, FocusableWidgetBase) or isinstance(w, MenuItem): #@TODO this is a hack find problem and fix
        #         self.focus_widgets.append(w)
        self.title = title
        self.title_widget = None
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
        self.title_widget = TitleWidget(self, "", "SomeTitle", 10, 1, "")
        self.title_widget.set_enclosing_window(self.data_entry_win)

        self.view_body = ViewBody(self.app, self.stdscr, self.data_entry_win, self.widgets)

        yb, xb = self.data_entry_win.getbegyx()
        for cols in self.view_body.widget_allocation.widget_columns:
            for wlo in cols.widget_layouts:
                w = wlo.widget
                x_begin = wlo.x_begin + xb
                y_begin = wlo.y_begin + yb
                sw = make_subwin(self.data_entry_win, w.get_height(), w.get_width(), wlo.y_begin, wlo.x_begin)
                w.set_enclosing_window(sw)

        self.view_menu = ViewMenu(self.app, self, self.stdscr, self.menu_win, self.menu_items)
        self.set_values(self.app.state)

    def get_values(self) -> Dict[str, Any]:
        """
        @return A dictionary object for the view.
        This consists of a dictionary:
        -   Which has an entry for each EditableWidget in the view.
        -   The keys are obtained from the widgets with the get_key() method
        -   and the values are most often of type str but can be Any and are obtained from  widget.get_value()
        Plus a boolean to indicate whether all the strings validated correctly.
        If any one widget value did not parse correctly the valid/ok boolean is set to false

        """
        v = {}
        ok = True
        for w in self.widgets:
            if is_editable(w):
                k = w.get_key()
                v[k] = cast(EditableWidgetBase, w).get_value()
        return v

    def set_values(self, state_values):
        
        vals = state_values
        for w in self.widgets:
            if is_editable(w):
                k = w.get_key()
                v = getattr(vals, k)
                w.set_value(v)

    def show(self):
        self.setup()

    def hide(self):
        self.outter_win.clear()

    def get_focus_widgets(self):
        widgets = self.focus_widgets if len(self.focus_widgets) != 0 else self.widgets + self.menu_items
        return widgets
        return self.widgets + self.menu_items

    def get_render_widgets(self):
        return [self.title_widget] + self.widgets + self.menu_items

    def render(self):
        for w in self.widgets + self.menu_items:
            w.render()
        ym, xm = self.outter_win.getmaxyx()
        xpos = (xm - len(self.title)) // 2
        self.outter_win.addstr(0, xpos, self.title, curses.A_BOLD)
        self.outter_win.noutrefresh()


from typing import List, Tuple, Dict, Any, cast
import curses
import curses.textpad

# import simple_curses.menu as M
from simple_curses.widget_base import *
from simple_curses.topmenu_widget import *
from simple_curses.layout import Rectangle, ColumnLayout, allocate_multiple_columns, TopmenuLayout
from simple_curses.validator import *
from simple_curses.title_widget import TitleWidget
from simple_curses.fig_widget import *
from simple_curses.menu import *
from simple_curses.kurses_ex import make_subwin
import simple_curses.window as Window

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

def validate_widgets(widgets):
    """Validate is a tow level list of list of WidgetBase"""
    pass

def min_body_size(widgets):
    pass

def flatten(list_of_lists):
    """
    Flatten a list of lists
    """
    if len(list_of_lists) == 0:
        return list_of_lists
    if isinstance(list_of_lists[0], list):
        return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
    return list_of_lists[:1] + flatten(list_of_lists[1:])


class BannerView:
    """A class that implements a view that dispays a single banner or info widget in the middle of the Form body. """

    def __init__(self, app, ident: str, label: str, stdscr, widget: WidgetBase):
        # the outter_win will contain all the dataentry fields and across the bottom the view menu
        self.stdscr = stdscr
        self.height, self.width = (widget.get_height(), widget.get_width())
        self.widget = widget
        self.label = label
        self.ident = ident
        self.app = app
    
    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def set_enclosing_window(self, win):
        self.outter_win = win
        self.outter_y_begin, self.outter_x_begin = win.getbegyx()

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
        tmp_h = w.get_height()
        tmp_w = w.get_width()
        tmp_y = yb + rbeg
        tmp_x = xb + cbeg
        widget_win = make_subwin(self.outter_win, w.get_height(), w.get_width(), rbeg, cbeg)
        w.set_enclosing_window(widget_win)

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

class DummyView:
    def _init__(self, figlet_icon: List[str], menu_widgets: List[TopMenuWidget]):
        pass

class TopmenuView:
    def __init__(self, app, figlet_widget: FigletWidget, menu_widgets: List[TopMenuWidget]):
        self.app = app
        self.icon = figlet_widget
        self.menu_items = menu_widgets
        self.widgets = [self.icon] + menu_widgets
        self.layout = TopmenuLayout(self.widgets)
        self.height, self.width = self.layout.get_size()
        self.has_focus = False

    def get_height(self):
        return self.height 
    
    def get_width(self):
        return self.width 
    
    def get_render_widgets(self):
        return self.widgets

    def get_focus_widgets(self):
        return self.menu_items

    def set_enclosing_window(self, win) -> None:
        self.win = win
        ybeg, xbeg = win.getbegyx()
        ym, xm     = win.getmaxyx()
        for layout in self.layout.widget_positions:
            ybeg, xbeg = layout.get_begin()
            h, w = (layout.widget.get_height(), layout.widget.get_width())
            subwin = make_subwin(win, layout.widget.get_height(), layout.widget.get_width(), ybeg, xbeg)
            layout.widget.set_enclosing_window(subwin)



    def focus_accept(self):
        selfhas_focus = True

    def focus_release(self):
        self.has_focus = False

    def handle_input(self, ch) -> bool:
        return False

    def render(self) -> None:
        for w in self.widgets:
            w.render()

class ViewMenu:
    """This is a Horizontal Stack, right justified, of menu items. Used to provide a menu inside a data entry view
    """

    def __init__(self, app, parent_view, stdscr, menu_win, menu_items: List[MenuItem]):
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

    def __init__(self, form, stdscr, win, widgets: List[WidgetBase]):
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


def menu_layout_and_enclose(menu_win, menu_items: List[MenuItem]):
    """
    Computes layout position of menus, makes subwindows for each menu item, and set_enclosing_window
    for each menu item

    NOTE: updates menu items
    """
    height, width = menu_win.getmaxyx()
    ybeg, xbeg = menu_win.getbegyx()
    max_item_width = 0
    total_width = 0
    item_width = None
    for m in menu_items:
        max_item_width = m.get_width() if max_item_width < m.get_width() else max_item_width
        total_width += m.get_width() + 4
    if (max_item_width + 2) * len(menu_items) < width:
        item_width = max_item_width + 2
    else:
        raise ValueError("cannot fit the menu items in a single line  with nice spacing")
    xpos = xbeg + width - item_width
    rectangles = []
    for m in reversed(menu_items):
        r = Rectangle(3, item_width - 2, ybeg + 1, xpos)  # leave a space between the menu items
        rectangles.append(r)
        xpos += -item_width
        tmp_win = menu_win.subwin(r.nbr_rows, r.nbr_cols, r.y_begin, r.x_begin)
        m.set_enclosing_window(tmp_win)
        m.has_focus = False

class DataEntryView:

    """A class that implements the detailed layout and function of a data entry view body body. A single app typically has a number of views
    that are swapped by the top menu or keyboard short cuts. This class represents the type of view that has data entry fields
    and an action menu at the bottom.
    
    This view and its companions ViewMenu and ViewBody perform the layout calculations

    """

    def __init__(self, 
                app, 
                ident: str, 
                title: str, 
                stdscr, 
                widgets: List[List[WidgetBase]],
                menu_items: List[MenuItem]):
        self.menu_height = 5
        self.title_height = 1
        self.view_menu = None
        self.view_body = None
        self.menu_win = None
        self.data_entry_win = None
        self.stdscr = stdscr

        self.menu_items = menu_items
        self.title = title
        self.title_widget = None
        self.ident = ident
        self.app = app
        #
        # DataEntryView consists of the following bits
        #   a title line
        #   1 line empty space under the title
        #   multi columned block for the widgets
        #   1 line empty space under widgets
        #   menu block, arranged horizontally and right justified
        #
        self.widget_allocation = allocate_multiple_columns(widgets)
        #self.height is height of title widgets and menu, the full inside of the body
        self.height = self.title_height + 1 + self.widget_allocation.get_height() + self.menu_height
        self.width = self.widget_allocation.get_width()
        #data_entry_height is height of the widgets without title or menus
        self.widgets_height = self.widget_allocation.get_height()
        self.flattened_widgets = flatten(widgets)
        self.focus_widgets = [w for w in (self.flattened_widgets + cast("List[WidgetBase]", self.menu_items)) if is_focusable(w) ]

    def get_height(self):
        return self.height
    
    def get_width(self):
        return self.width

    def set_enclosing_window(self, win):
        self.outter_win = win

    def setup(self):
        mark_territory = False

        # TODO - allocate excess height and width
        yb, xb = self.outter_win.getbegyx()
        ym, xm = self.outter_win.getmaxyx()
        excess_height = ym - self.height
        excess_width  = xm - self.width
        excess_after_title = 1
        excess_after_widgets = 1
        # if excess_height > 0:
        #     excess_after_title = 1 + excess_height // 2
        #     excess_after_widgets = 1 + excess_height // 2


        # self.menu_win = curses.newwin(self.menu_height, self.width, self.outter_y_begin + self.data_entry_height, 0)
        # self.widgets_win = curses.newwin(self.widgets_height, self.width, self.outter_y_begin + 1, 0)
        self.title_win   = Window.newwin_inside(self.outter_win, 1, self.width, 0, 0)
        if mark_territory:
            self.title_win.bkgd("*")
            self.title_win.refresh()

        self.widgets_win = Window.newwin_after (self.title_win, self.widgets_height, self.width, 1, excess_after_title)
        if mark_territory:
            self.widgets_win.bkgd("*")
            self.widgets_win.refresh()

        self.menu_win    = Window.newwin_after (self.widgets_win, self.menu_height,    self.width, 1, excess_after_widgets)
        if mark_territory:
            self.menu_win.bkgd("X")
            self.menu_win.refresh()

        self.title_widget = TitleWidget(self, "", "SomeTitle", 10, 1, "")
        self.title_widget.set_enclosing_window(self.title_win)


        for cols in self.widget_allocation.widget_columns:
            for wlo in cols.widget_layouts:
                w = wlo.widget
                x_begin = wlo.x_begin + xb
                y_begin = wlo.y_begin + yb
                sw = make_subwin(self.widgets_win, w.get_height(), w.get_width(), wlo.y_begin, wlo.x_begin)
                w.set_enclosing_window(sw)

        menu_layout_and_enclose(self.menu_win, self.menu_items)
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
        for w in self.flattened_widgets:
            if is_editable(w):
                k = w.get_key()
                v[k] = cast(EditableWidgetBase, w).get_value()
        return v

    def set_values(self, state_values):
        
        vals = state_values
        for w in self.flattened_widgets:
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
        return [self.title_widget] + self.flattened_widgets + self.menu_items

    def render(self):
        ym, xm = self.outter_win.getmaxyx()
        xpos = (xm - len(self.title)) // 2
        self.outter_win.addstr(0, xpos, self.title, curses.A_BOLD)
        self.outter_win.refresh()
        for w in self.flattened_widgets + self.menu_items:
            w.render()
        self.widgets_win.refresh()
        self.menu_win.refresh()


from typing import List, Tuple, Dict, Any, cast
import sys
import curses
import curses.textpad

from simple_curses.widget_base    import is_editable, is_focusable, WidgetBase, FocusableWidgetBase, EditableWidgetBase
from simple_curses.layout         import Rectangle, allocate_multiple_columns, TopmenuLayout
from simple_curses.validator      import *
from simple_curses.kurses_ex      import make_subwin
import simple_curses.window       as     Window
from simple_curses.keyboard       import FunctionKeys

from simple_curses.widgets.topmenu_widget   import *
from simple_curses.widgets.blocktext_widget import HelpWidget
from simple_curses.widgets.title_widget     import TitleWidget
from simple_curses.widgets.blocktext_widget import *
from simple_curses.widgets.fig_widget       import *


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
        self.menu_items = []
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

    def handle_input(self, key):
        return False

    def render(self):
        self.widget.render()

class DummyView:
    def _init__(self, figlet_icon: List[str], menu_widgets: List[TopMenuWidget]):
        pass

class HelpView(BannerView):
    def __init__(self, app, ident, label, stdscr):
        super().__init__(app, ident, label, stdscr, HelpWidget(app))

    
class TopmenuView:
    def __init__(self, app, figlet_widget: FigletWidget, menu_widgets: List[TopMenuWidget]):
        self.app = app
        self.icon = figlet_widget
        self.menu_items = menu_widgets
        self.widgets = [self.icon] + menu_widgets
        self.layout = TopmenuLayout(self.widgets)
        self.height, self.width = self.layout.get_size()
        self.has_focus = False
        self.focus_index = 0

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

    def get_menu_by_view(self, view):
        for m in self.menu_items:
            if m.view is view:
                return m
        raise ValueError("failed to find view {} in top menu".format(view.ident))

    def handle_input(self, key):
        return False

    def focus_accept(self):
        selfhas_focus = True

    def focus_release(self):
        self.has_focus = False

    def handle_input(self, ch) -> bool:
        return False

    def render(self) -> None:
        for w in self.widgets:
            w.render()

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
        self.app = app
        self.menu_height = 5
        self.title_height = 1
        self.view_menu = None
        self.view_body = None
        self.menu_win = None
        self.data_entry_win = None
        self.stdscr = stdscr

        self.menu_items = menu_items
        self.function_keys = FunctionKeys()
        for m in self.menu_items:
            self.function_keys.add_accelerator(m.accelerator_key, m)

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
        # self.focus_widgets = [w for w in (self.flattened_widgets + cast("List[WidgetBase]", self.menu_items)) if is_focusable(w) ]
        self.focus_index = 0
        self.focus_widgets = self.flattened_widgets

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

    def shift_focus_to(self, w_index):
        old_focus_widget = self.focus_widgets[self.focus_index]
        self.focus_index = w_index
        old_focus_widget.focus_release()
        focus_widget = self.focus_widgets[self.focus_index]
        focus_widget.focus_accept()

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

    def handle_input(self, key):
        did_handle = True
        if is_next_control(key):
            w_index = (self.focus_index + 1 + len(self.focus_widgets)) % (len(self.focus_widgets))
            self.shift_focus_to(w_index)
        elif is_prev_control(key):
            w_index = (self.focus_index - 1 + len(self.focus_widgets)) % (len(self.focus_widgets))
            self.shift_focus_to(w_index)
        elif self.function_keys.is_function_key(key):
            m = self.function_keys.get_menu(key)
            if m is not None:
                m.invoke()
        else: 
            did_handle = self.flattened_widgets[self.focus_index].handle_input(key)
        return did_handle

    def render(self):
        ym, xm = self.outter_win.getmaxyx()
        xpos = (xm - len(self.title)) // 2
        self.outter_win.addstr(0, xpos, self.title, curses.A_BOLD)
        self.outter_win.refresh()
        for w in self.flattened_widgets + self.menu_items:
            w.render()
        self.widgets_win.refresh()
        self.menu_win.refresh()

def quit_function(app, view):
    sys.exit()

class QuitView(DataEntryView):
    def __init__(self, app, ident: str, title: str, stdscr):
        widgets = [
            [
                BlockTextWidget(app, ["Are you sure you want to quit ??", "If so hit ^F1"])
            ]
        ]
        menu_items = [
            MenuItem(app, "quit_view_menu", 3, FKEY_CTRL_F1, quit_function, "")
        ]
        super().__init__(app, ident, title, stdscr, widgets, menu_items)

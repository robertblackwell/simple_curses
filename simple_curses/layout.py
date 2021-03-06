from typing import List, Dict
import curses
from simple_curses.widget_base import WidgetBase
from simple_curses.widgets.topmenu_widget import MenuItem
class HStack:
    pass


class VStack:
    def __init__(self, win, widgets: List[WidgetBase]):
        pass


PAD_X_START = 1
PAD_X_BETWEEN = 1
PAD_X_END = 1
PAD_Y_START = 0
PAD_Y_BETWEEN = 0
PAD_Y_END = 0



class Rectangle:
    """
    A rectangular sub-region of the screen or window
    """

    def __init__(self, nbr_rows, nbr_cols, y_beg=0, x_beg=0):
        self.nbr_rows = nbr_rows
        self.nbr_cols = nbr_cols
        self.y_begin = y_beg
        self.x_begin = x_beg
    def get_height(self):
        return self.height
    def get_width(self):
        return self.width


class WidgetLayout:
    """
    represents the rectangle allocated to contain a widget
    y_begin and x_begin attributes are relative starting coordinates
    good for use with the kurses_ex function make_subwin()

    relative to what ?

    """

    def __init__(self, w: WidgetBase, y_begin, x_begin, y_max, x_max):
        self.widget = w

        self.y_begin = y_begin #"y_begin - is relative to the rectangle used in ColumnLayout"
        self.x_begin = x_begin #"x_begin - is relative to the rectangle used in ColumnLayout"
        self.ymax = y_max
        self.xmax = x_max
        if self.ymax < w.get_height():
            raise ValueError("ymax: {}, w.get_height(): {}".format(self.ymax, w.get_height()))
        if self.xmax < w.get_width():
            raise ValueError("xmax: {}, w.get_width(): {}".format(self.xmax, w.get_width()))

    def get_width(self):
        return self.xmax
    def get_height(self):
        return self.ymax


class WidgetColumn:
    def __init__(self, height, width, widget_layouts: List[WidgetLayout]):
        self.height = height
        self.width = width
        self.widget_layouts = widget_layouts

    def get_height(self):
        return self.height
    def get_width(self):
        return self.width
    # def get_ymax(self):
    #     h = 0
    #     for wl in self.widget_layouts:
    #         h += wl.get_height()
    #     return h
    # def get_height(self):
    #     h = 0
    #     for wl in self.widget_layouts:
    #         h += wl.get_height()
    #     return h

    # def get_width(self):
    #     max = 0
    #     for wl in self.widget_layouts:
    #         max = wl.get_width() if wl.get_width() > max else max
    #     return max

    def widget_count(self):
        return len(self.widget_layouts)

class WidgetAllocation:
    def __init__(self):
        self.widget_columns: List[WidgetColumn] = []
        pass

    def add_widget_column(self, widget_column: WidgetColumn):
        self.widget_columns.append(widget_column)

    def get_ymax(self):
        m = 0
        for wc in self.widget_columns:
            h = wc.get_height()
            m = h if h > m else m
        return m
    def get_height(self):
        return self.get_ymax()

    def get_width(self):
        width = 0
        for col in self.widget_columns:
            width += col.get_width()
        return width

    def column_count(self):
        return len(self.widget_columns)

def single_column(widgets : List[WidgetBase]):
    """
    Computes the smallest rectangle that will contain the given
    list of widget as a single column
    """
    layouts = []
    rows = PAD_Y_START
    cols = 0
    for w in widgets:
        lout = WidgetLayout(w, rows, PAD_X_START, w.get_height(), w.get_width())
        layouts.append(lout)
        rows += w.get_height() + PAD_Y_BETWEEN
        tmp = PAD_X_START + w.get_width() + PAD_X_END
        cols = tmp if tmp > cols else cols

    return WidgetColumn(rows + PAD_Y_END - PAD_Y_BETWEEN, cols, layouts)

def allocate_multiple_columns(columns: List[List[WidgetBase]]):
    wth = 0
    h = 0
    walloc = WidgetAllocation()
    cols = 0
    xbeg = PAD_X_START
    for column in columns:
        layouts = []
        rows = PAD_Y_START
        for w in column:
            lout = WidgetLayout(w, rows, xbeg, w.get_height(), w.get_width())
            layouts.append(lout)
            rows += w.get_height() + PAD_Y_BETWEEN
            tmp2 = w.get_width()
            tmp = PAD_X_START + w.get_width() + PAD_X_END
            cols = tmp if tmp > cols else cols
        wc = WidgetColumn(rows + PAD_Y_END - PAD_Y_BETWEEN, cols, layouts)
        xbeg += cols
        wth += cols
        h = rows if rows > h else h
        walloc.add_widget_column(wc)
    return walloc


def layout_viewmenu(menu_win, menu_items: List[MenuItem]) -> Dict[MenuItem, Rectangle]:
    """
    Computes layout position of menus, makes subwindows for each menu item, and set_enclosing_window
    for each menu item

    NOTE: updates menu items
    NOTE: move to layout.py - modify to return something and perform set_enclosing_win in View
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
    rectangles = {}
    for m in reversed(menu_items):
        r = Rectangle(3, item_width - 2, ybeg + 1, xpos)  # leave a space between the menu items
        rectangles[m] = r
        xpos += -item_width
        # tmp_win = menu_win.subwin(r.nbr_rows, r.nbr_cols, r.y_begin, r.x_begin)
        # m.set_enclosing_window(tmp_win)
        # m.has_focus = False
    return rectangles


# class ColumnLayout:
#     """Takes a list of widgets and arranges them into columns so that they will fit into
#     the rectangle formed by the constructors max_height and max_width paramters.

#     Makes sure that no column is wider than max_widget_width

#     Uses the padding constants at the top of this file
#     """

#     def __init__(self, max_height, max_widget_width):
#         self.widget_allocation = WidgetAllocation()
#         self.current_column = []
#         self.col_width = 0
#         self.col_height = PAD_Y_START
#         self.y_begin = self.col_height
#         self.x_begin = PAD_X_START
#         self.w_index = 0
#         self.max_height = max_height
#         self.max_widget_width = max_widget_width
#         self.widgets = None

#     def column_count(self):
#         """returns the number of columns"""
#         return self.widget_allocation.column_count()

#     def widget_count(self, column_index):
#         """Returns the number of widgets in the column with the given index"""
#         if column_index >= self.column_count():
#             raise RuntimeError("column index {} is out of bounds".format(column_index))
#         return len(self.widget_allocation.widget_columns[column_index].widget_layouts)

#     def get_widget_layout(self, column_index, widget_index):
#         """get the layout for a widget by index.
#         """
#         if column_index >= self.column_count():
#             raise RuntimeError("column index {} is out of bounds".format(column_index))
#         if widget_index >= self.widget_count(column_index):
#             raise RuntimeError("widget index {} is out of bounds".format(widget_index))
#         return self.widget_allocation.widget_columns[column_index].widget_layouts[widget_index]

#     def get_ymax(self):
#         return self.widget_allocation.get_ymax()

#     def next_column(self):
#         self.current_column = []
#         self.col_height = PAD_Y_START
#         self.y_begin = self.col_height
#         self.x_begin = self.x_begin + self.max_widget_width + PAD_X_START
#         self.col_width = 0

#     def add_widget_to_layout(self, w):
#         wl = WidgetLayout(w, self.y_begin, self.x_begin, w.get_height() + PAD_Y_BETWEEN, w.get_width() + PAD_X_BETWEEN)
#         # print("adding widget to layout y_begin:{} x_begin: {} ymax: {} xmax: {}"
#         #   .format(wl.y_begin, wl.x_begin, wl.ymax, wl.xmax))
#         self.current_column.append(wl)
#         self.col_height += w.get_height() + PAD_Y_BETWEEN
#         self.y_begin = self.col_height
#         self.col_width = w.get_width() + PAD_X_BETWEEN if self.col_width < w.get_width() + PAD_X_BETWEEN else self.col_width

#     def add_current_column_to_allocation(self):
#         self.widget_allocation.add_widget_column(WidgetColumn(self.col_height, self.col_width, self.current_column))

#     def add_widget_to_allocation(self, w):
#         return self.col_height + w.get_height() + PAD_Y_BETWEEN > self.max_height

#     def is_last(self):
#         return self.w_index == len(self.widgets) - 1

#     def would_overflow(self, w):
#         return self.col_height + w.get_height() + PAD_Y_BETWEEN > self.max_height

#     def widget_to_tall(self, w):
#         return w.get_height() + PAD_Y_BETWEEN > self.max_height

#     def assign_to_columns(self):
#         pass

#     def calc_max_width(self):
#         m = 0
#         for w in self.widgets:
#             tmp = w.get_width() + PAD_X_BETWEEN
#             m = tmp if tmp > m else m
#         return m

#     def assign_x_coord(self):
#         pass

#     def add_widgets(self, widgets):
#         self.widgets = widgets
#         while self.w_index < len(self.widgets):
#             w = widgets[self.w_index]
#             if self.widget_to_tall(w):
#                 raise RuntimeError(
#                     "widget too tall index:{} w.height {}".format(self.w_index, w.get_height() + PAD_Y_BETWEEN))
#             # self.col_height += w.get_height()
#             self.y_begin = self.col_height
#             # self.col_width = w.get_width() + PAD_X_BETWEEN if self.col_width < w.get_width() + PAD_X_BETWEEN else 
#             # self.col_width 
#             if self.would_overflow(w) and not self.is_last():
#                 self.add_current_column_to_allocation()
#                 self.next_column()
#                 self.add_widget_to_layout(w)
#             elif self.would_overflow(w) and self.is_last():
#                 self.add_current_column_to_allocation()
#                 self.next_column()
#                 self.add_widget_to_layout(w)
#                 self.add_current_column_to_allocation()
#             elif self.is_last():
#                 self.add_widget_to_layout(w)
#                 self.add_current_column_to_allocation()
#             else:
#                 self.add_widget_to_layout(w)
#             self.w_index += 1

class WidgetPosition:
    def __init__(self, beg_y, beg_x, widget):
        self.beg_y = beg_y
        self.beg_x = beg_x
        self.widget = widget
    def get_begin(self):
        return (self.beg_y, self.beg_x)

# class VerticalStack:
#     def __init__(self, begin_pos, max_pos, widgets):
#         self.begin_row = begin_pos[0]
#         self.begin_col = begin_pos[1]
#         self.max_row = max_pos[0]
#         self.max_col = max_pos[1]

#         self.widgets = widgets
#         self.widget_positions = None

#     def vertical_space(self):
#         rows = 0
#         max_width = 0
#         for w in self.widgets:
#             rows += w.get_height()
#             max_width = w.get_width() if w.get_width() > max_width else max_width

#         available_rows = (self.max_row - self.begin_row)
#         available_width = (self.max_col - self.begin_col)
#         excess_rows = available_rows - rows
#         excess_width = available_width - max_width

#         if excess_rows <= 0:
#             raise ValueError(
#                 "LayoutVerticcalStack.required_space  requires too many rows rows required : {}  rows available rows "
#                 "{}".format( 
#                     rows, available_rows))
#         if excess_width <= 0:
#             raise ValueError(
#                 "LayoutVerticcalStack.required_space  requires too much width  width required : {}  width available "
#                 "rows {}".format( 
#                     max_width, available_width))

#         start_row = self.begin_row + (2 if excess_rows > 2 else excess_rows)
#         start_col = self.begin_col
#         self.widget_positions = []
#         for w in self.widgets:
#             wp = WidgetPosition(start_row, start_col, w)
#             self.widget_positions.append(wp)
#             start_row += w.get_height()

#     def compute_layout(self):
#         self.vertical_space()
#         return self.widget_positions

class TopmenuLayout:
    def __init__(self, menuiwidgets: List[WidgetBase]):
        self.height = 0
        for m in menuiwidgets:
            self.height = m.get_height() if m.get_height() > self.height else self.height
        
        self.widget_positions = []
        col = PAD_X_START
        for m in menuiwidgets:
            self.widget_positions.append(WidgetPosition(0, col, m))
            col += m.get_width() + PAD_X_BETWEEN
            self.height = m.get_height() if m.get_height() > self.height else self.height
        self.width = col

    def get_height(self):
        return self.height
    def get_width(self):
        return self.width
    def get_size(self):
        return (self.get_height(), self.get_width())

# class HorizontalStack:
#     def __init__(self, max_pos, widgets):
#         self.widget_positions = None
#         self.begin_row = 0  # begin_pos[0]
#         self.begin_col = 0  # begin_pos[1]
#         self.max_row = max_pos[0]
#         self.max_col = max_pos[1]

#         self.widgets = widgets
#         self.widget_positons = None

#     def horizontal_space(self):
#         cols = 0
#         max_height = 0
#         for w in self.widgets:
#             cols += w.get_width()
#             max_height = w.get_height() if w.get_height() > max_height else max_height

#         available_cols = (self.max_col + 1 - self.begin_col)
#         available_height = (self.max_row + 1 - self.begin_row)
#         excess_cols = available_cols - cols
#         excess_height = available_height - max_height

#         if excess_cols < 0:
#             raise ValueError(
#                 "LayoutHorizontalStack.required_space  requires too many cols   cols_required  : {}  cols available   "
#                 "{}".format( 
#                     cols, available_cols))
#         if excess_height < 0:
#             raise ValueError(
#                 "LayoutVerticcalStack.required_space  requires too much height  height_required : {}  available "
#                 "height {}".format( 
#                     max_height, available_height))

#         n = len(self.widgets)
#         cspace = (excess_cols // n)
#         fromt_space = 0
#         if cspace >= 0:
#             front_space = cspace // 2
#         else:
#             cspace = 0
#             front_space = excess_cols // 2

#         start_row = self.begin_row
#         start_col = self.begin_col + front_space
#         self.widget_positions = []
#         for w in self.widgets:
#             wp = WidgetPosition(start_row, start_col, w)
#             self.widget_positions.append(wp)
#             start_col += cspace + w.get_width()

#     def compute_layout(self):
#         self.horizontal_space()
#         return self.widget_positions

import curses
import curses.textpad
import string

import string_buffer
from colors import Colors



class WidgetPosition:
    def __init__(self, beg_y, beg_x, widget):
        self.beg_y = beg_y
        self.beg_x = beg_x
        self.widget = widget

class VerticalStack:
    def __init__(self, begin_pos, max_pos, widgets):
        self.begin_row = begin_pos[0]
        self.begin_col = begin_pos[1]
        self.max_row = max_pos[0]
        self.max_col = max_pos[1]

        self.widgets = widgets
        self.widget_positions = None

    def vertical_space(self):
        rows = 0
        max_width = 0
        for w in self.widgets:
            rows += w.get_height()
            max_width = w.get_width() if w.get_width() > max_width else max_width

        available_rows = (self.max_row - self.begin_row)
        available_width = (self.max_col - self.begin_col)
        excess_rows = available_rows - rows
        excess_width = available_width - max_width

        if excess_rows <= 0:
            raise ValueError("LayoutVerticcalStack.required_space  requires too many rows rows required : {}  rows available rows {}}".format(rows, available_rows))
        if excess_width <= 0:
            raise ValueError("LayoutVerticcalStack.required_space  requires too much width  width required : {}  width available rows {}}".format(max_width, available_width))

        start_row = self.begin_row + (2 if excess_rows > 2 else excess_rows)
        start_col = self.begin_col
        self.widget_positions = []
        for w in self.widgets:
            wp = WidgetPosition(start_row, start_col, w)
            self.widget_positions.append(wp)
            start_row += w.get_height()
        
    def compute_layout(self):
        self.vertical_space()
        return self.widget_positions


class HorizontalStack:
    def __init__(self, max_pos, widgets):
        self.begin_row = 0 #begin_pos[0]
        self.begin_col = 0 #begin_pos[1]
        self.max_row = max_pos[0]
        self.max_col = max_pos[1]

        self.widgets = widgets
        self.widget_positons = None

    def horizontal_space(self):
        cols = 0
        max_height = 0
        for w in self.widgets:
            cols += w.get_width()
            max_height = w.get_height() if w.get_height() > max_height else max_height

        available_cols = (self.max_col + 1 - self.begin_col)
        available_height = (self.max_row + 1 - self.begin_row)
        excess_cols = available_cols - cols
        excess_height= available_height - max_height

        if excess_cols < 0:
            raise ValueError("LayoutHorizontalStack.required_space  requires too many cols   cols_required  : {}  cols available   {}}".format(cols, available_cols))
        if excess_height < 0:
            raise ValueError("LayoutVerticcalStack.required_space  requires too much height  height_required : {}  available height {}}".format(max_height, available_height))

        n = len(self.widgets)
        cspace = (excess_cols // n)
        fromt_space = 0
        if cspace >= 0:
            front_space = cspace // 2
        else:
            cspace = 0
            front_space = excess_cols // 2

        start_row = self.begin_row
        start_col = self.begin_col + front_space
        self.widget_positions = []
        for w in self.widgets:
            wp = WidgetPosition(start_row, start_col, w)
            self.widget_positions.append(wp)
            start_col += cspace + w.get_width()
        
    def compute_layout(self):
        self.horizontal_space()
        return self.widget_positions


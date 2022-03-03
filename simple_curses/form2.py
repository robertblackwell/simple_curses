import curses
import curses.textpad
import string

import string_buffer
from colors import Colors

def is_next_control(ch):
    return (ch == "KEY_RIGHT")

def is_prev_control(ch):
    return (ch == "KEY_LEFT")

def is_function_key(ch):
    tmp = ch[0:6]
    return (tmp == "KEY_F(")

def fn_key_match(k1, k2):
    return (k1 == k2)

def fn_key_description(k1):
    s1 = k1.replace("KEY_F(", "")
    s2 = s1.replace(")", "")
    s3 = "F"+s2
    return s3


class WidgetPosition:
    def __init__(self, beg_y, beg_x, widget):
        self.beg_y = beg_y
        self.beg_x = beg_x
        self.widget = widget

class LayoutVerticalStack:
    def __init__(self, begin_pos, max_pos, widgets):
        self.begin_row = begin_pos[0]
        self.begin_col = begin_pos[1]
        self.max_row = max_pos[0]
        self.max_col = max_pos[1]

        self.widgets = widgets
        self.widget_positons = None

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

        start_row = self.beg_y + (2 if excess_rows > 2 else excess_rows)
        start_col = self.begin_col
        self.widget_positions = []
        for w in self.widgets:
            wp = WidgetPosition(start_row, start_col, w)
            self.widget_positions.append(wp)
            start_row + w.get_height()
        
    def compute_layout(self):
        self.vertical_space()
        return self.widget_positions()


class HorizontalStack:
    def __init__(self, begin_pos, max_pos, widgets):
        self.begin_row = begin_pos[0]
        self.begin_col = begin_pos[1]
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

        available_cols = (self.max_col - self.begin_col)
        available_height = (self.max_row - self.begin_row)
        excess_cols = available_cols - cols
        excess_height= available_height - max_height

        if excess_cols <= 0:
            raise ValueError("LayoutHorizontalStack.required_space  requires too many cols   cols_required  : {}  cols available   {}}".format(cols, available_cols))
        if excess_height <= 0:
            raise ValueError("LayoutVerticcalStack.required_space  requires too much height  height_required : {}  available height {}}".format(max_height, available_height))

        n = len(self.widgets)
        cspace = (excess_cols // n)
        fromt_space = 0
        if cspace >= 0:
            front_space = excess_cols - n*cspace
        else:
            cspace = 0
            front_space = excess_cols // 2

        start_row = self.beg_y + 1
        start_col = self.begin_col + front_space
        self.widget_positions = []
        for w in self.widgets:
            wp = WidgetPosition(start_row, start_col, w)
            self.widget_positions.append(wp)
            start_col += cspace
        
    def compute_layout(self):
        self.horizontal_space()
        return self.widget_positons


class Form2:
    def __init__(self, stdscr, left_widgets, right_widgets, context):
        self.stdscr = stdscr
        stdscr.bkgd(" ", curses.color_pair(5))
        mx = stdscr.getmaxyx()
        self.height = mx[0] - 2
        self.width = mx[1] - 2

        self.left_widgets = left_widgets
        self.right_widgets = right_widgets

        self.context = context
        self.focus_index = 0
        self.title = "This is a data entry form"

        self.title_start_row = 0
        self.title_start_col = 0
        self.title_height = 5
        self.title_width = self.width
        self.outter_win = stdscr.subwin(self.height + 2, self.width + 2, 0, 0)
        self.inner_win = self.outter_win.subwin(self.height, self.width, 1, 1)
        self.title_win = curses.newwin(self.title_height, self.title_width, 0, 0)

        self.menu_height = 5
        self.msg_height = 5


        self.body_start_row = self.title_start_row + self.title_height
        self.body_start_col = 0
        self.body_width = self.width
        self.body_height = self.height - self.title_height - self.msg_height + 2

        self.menu_start_row = self.body_start_row + self.body_height - 1
        self.menu_width = self.width
        self.menu_height = 5

        self.msg_start_row = self.menu_start_row + self.menu_height - 1
        self.msg_width = self.width
        self.msg_height = 5

        self.menu_height = 5
        self.msg_height = 5

        body_start_row = 4
        body_start_col = 0

        self.body_win = curses.newwin(self.body_height, self.width, self.title_height - 1, 0 )
        self.msg_win = curses.newwin(self.msg_height, self.width, body_start_row + self.body_height - 1, 0 )
        self.message_text = ""
        body_height = 0
        col = body_start_col + 4  
        for w in self.widgets:
            klass = w.__class__.__name__
            if klass == "MenuItem":
                w.set_enclosing_window(curses.newwin(w.get_height(), w.get_width(), w.row, col))
                col += w.get_width() + 4
            else:
                w.start_row = w.row + body_start_row
                w.start_col = w.col + body_start_col
                w.set_enclosing_window(curses.newwin(w.get_height(), w.get_width(), self.body_start_row + w.row, self.body_start_col + w.col ))
            w.set_form(self)
            w.has_focus = False
        zz = self.body_win.getparyx()
        z2 = self.title_win.getparyx()
        z3 = z2


    def msg_error(self, msg):
        label = " ERROR: "
        self.msg_win.clear()
        self.msg_win.addstr(1, 1, label, Colors.msg_error_attr())
        self.msg_win.addstr(1, 1 + len(label), msg)
        self.msg_win.noutrefresh()
        curses.doupdate()

    def msg_warn(self, msg):
        label = " WARNING: "
        self.msg_win.clear()
        self.msg_win.addstr(1, 1, label )
        self.msg_error.addstr(1, 1 + len(label), msg)
        self.msg_win.noutrefresh()
        curses.doupdate()

    def msg_info(self, msg):
        label = " INFO: "
        self.msg_win.clear()
        self.msg_win.addstr(1, 1 , label )
        self.msg_win.addstr(1, 1 + len(label), msg)
        self.msg_win.noutrefresh()
        curses.doupdate()

    def handle_input(self):
        # here should render everything to ensure the latest version of the screen is being seen
        # hen input is provided
        ch = self.stdscr.getkey()
        self.msg_info("handle_input ch: {} len(ch) {} hex: {}".format(ch, len(ch), ch.encode('utf8').hex()))
        focus_widget = self.widgets[self.focus_index]
        focus_widget.focus_accept()
        if focus_widget.handle_input(ch):
            return
        else:
            if is_next_control(ch):
                old_focus_widget = self.widgets[self.focus_index]
                self.focus_index = (self.focus_index + 1 + len(self.widgets)) % (len(self.widgets))
                old_focus_widget.focus_release()
                focus_widget = self.widgets[self.focus_index]
                focus_widget.focus_accept()
            elif is_prev_control(ch):
                old_focus_widget = self.widgets[self.focus_index]
                self.focus_index = (self.focus_index - 1 + len(self.widgets)) % (len(self.widgets))
                old_focus_widget.focus_release()
                focus_widget = self.widgets[self.focus_index]
                focus_widget.focus_accept()
            elif is_function_key(ch):
                self.handle_menu(ch)

    def box_form(self):
        self.stdscr.border(0,0,0,0,0,0,0)

    def make_boxes(self):
        # self.stdscr.border(0,0,0,0,0,0,0)
        self.title_win.border(0,0,0,0,0,0,0,0)
        self.body_win.border(0,0,0,0, curses.ACS_LTEE, curses.ACS_RTEE,0,0)
        # self.menu_win.border(0,0,0,0, curses.ACS_LTEE, curses.ACS_RTEE, curses.ACS_LTEE, curses.ACS_RTEE)
        self.msg_win.border(0,0,0,0, curses.ACS_LTEE, curses.ACS_RTEE, 0, 0)


    def render_message(self):
        pass
        self.msg_win.addstr(1,1, " Msg: ", Colors.msg_label_attr())

    def render(self):
        self.make_boxes()
        self.title_win.addstr(2, (self.width // 2) - (len(self.title) // 2), self.title, Colors.title_attr())
        self.msg_win.addstr(1,1, " Msg: ", Colors.msg_label_attr())
        self.title_win.noutrefresh()
        self.body_win.noutrefresh()
        # self.menu_win.noutrefresh()
        self.msg_win.noutrefresh()

        for w in self.widgets:
            w.render()

        self.render_message()
        # nbr_menuitems = len(self.menus)
        # cols_per_item = (self.width - 2) // nbr_menuitems
        # start = 1
        # for m in self.menus:
        #     self.menu_win.move(1,start)
        #     m.render()
        #     start += cols_per_item

        # self.menu_win.noutrefresh()

        curses.doupdate()
        # self.stdscr.refresh()

    def run(self):
        self.widgets[self.focus_index].focus_accept()
        self.render()
        while True:
            self.render()
            self.handle_input()

    def get_values(self):
        result = {}
        ok = True
        for w in self.widgets:
            # b1 = hasattr (w, "validator") 
            # b2 = hasattr(w, "id") 
            # b3 = hasattr(w, "get_value") 
            # b4 = callable(getattr(w.__class__, "get_value"))
            if hasattr(w, "validator") and hasattr(w, "id") and hasattr(w, "get_value") and callable(getattr(w, "get_value")) :
                v = w.get_value()
                tmp = w.validator.validate(v) 
                if tmp is not None:
                    result[w.id] = tmp
                    ok = ok and True
                else:
                    ok = ok and False
                    self.msg_error(w.validator.error_message())    

        return result if ok else None


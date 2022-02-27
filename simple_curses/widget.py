import time
import sys
import curses
import curses.textpad
import time
import string

import string_buffer

menu = ['Home', 'Store Lookup', 'MAC Lookup', 'MAC Clear',
        'Afterhours Wi-Fi Disable/Enable', 'Exit']



requiredHeight = 15
requiredWidth = 60


# 
# tests an input string to see if it represents an editing character
# 
def is_edit_character(ch):
    pass
def is_edit_back(ch):
    return (len(ch) == 1) and (ch[0] == '\x7f')

def is_edit_del(ch):
    return (ch == "KEY_DC")

def is_move_left(ch):
    return (ch == "KEY_SLEFT")

def is_move_right(ch):
    return (ch == "KEY_SRIGHT")


# A basic text widget that allows the entry of printable characters.
# A model upon which to base more complicated text controls
# A TextWidget is composed of a label and an value field
class TextWidget:
    def __init__(self, row, col, label, width, attributes, data):
        self.has_focus = False
        self.row = row
        self.col = col
        self.data = data
        self.content = ""
        self.content_position = 0
        self.label = label + ": "
        self.width = width
        self.height = 1
        self.attributes = attributes
        self.form = None
        tmp = width + len(self.label)
        # self.win = curses.newwin(1, width + len(self.label) + 2, row, col, )
        self.string_buffer = string_buffer.StringBuffer("", self.width)

        # these properties are for manaing the display of the conttent string during
        # entry and editing
        self.display_content_start = 0
        self.display_content_position = 0 #current cursor position in the content
        self.display_cursor_position = 0 # always between 0 .. width - that is always visible
        self.display_length = 0 # is width-1 if we are adding to the end of the string in which case the cursor is over the 'next' slot
                                # if we are editing the string and the cursor is somewhere inside the content string then has the value width
    
    # paint attributes for the content area so that it is visible to used
    def paint_content_area_background(self):
        tmp = self.width + len(self.label) - 1
        for i in range(0, tmp):
            if self.has_focus:
                self.win.addstr(0, i, "_")
            else:
                self.win.addstr(0, i, "_")

    # called by the containing form to paint/render the Widget
    def render(self):
        self.paint_content_area_background()
        self.win.addstr(0, 0, self.label, curses.A_BOLD)
        self.win.addstr(0, len(self.label), self.string_buffer.display_string)
        if self.has_focus:
            self.position_cursor()
        self.win.noutrefresh()
    
    # 
    # Positions the cursor to the current active position and makes sure it blinks.
    # The current active position is usually 1 space past the end of the currently input text
    # 
    def position_cursor(self):
        ch_under_cursor = self.string_buffer.display_string[self.string_buffer.cpos_buffer]
        self.win.addnstr(0, len(self.label) + self.string_buffer.cpos_buffer, ch_under_cursor, 1, curses.A_REVERSE + curses.A_BLINK)
        self.win.noutrefresh()
    # 
    # called by the Form instance to give this control focus
    # 
    def focus_accept(self):
        self.has_focus = True
        self.position_cursor()

    def focus_release(self):
        self.has_focus = False

    # 
    # Called by inpput handling functions to signal to user that the last keysttroke was
    # invalid. Dont quite know what to do yet
    # 
    def invalid_input(self):
        pass
    # When a Widget has the focus every keystroke (with some small exceptions)
    # get passed to this function.
    # If the Widget handles the keystroke then it should return true
    # else should return false
    # 
    def handle_input(self, ch):
        did_handle_ch = True
        if (len(ch)  == 1) and (ch[0] in string.printable):
            self.string_buffer.handle_character(ch)
        elif is_edit_back(ch):
            self.string_buffer.handle_backspace()
        elif is_edit_del(ch):
            self.string_buffer.handle_delete()
        elif is_move_left(ch):
            self.string_buffer.handle_left()
        elif is_move_right(ch):
            self.string_buffer.handle_right()
        else:
            did_handle_ch = False

        self.position_cursor()
        return did_handle_ch

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

class MenuItem:
    def __init__(self, name, fn_key, function):
        self.name = name
        self.fn_key = fn_key
        self.function = function
        self.form = None
        self.win = None
    def invoke(self, fn_key, context):
        self.function(self.form, context)
    
    def render(self):
        self.win.addstr(fn_key_description(self.fn_key)+"-", curses.color_pair(self.form.COLOR_GREEN_BLACK) + curses.A_BOLD)
        self.win.addstr(self.name, curses.color_pair(self.form.COLOR_CYAN_BLACK) + curses.A_BOLD)


class Form:
    def __init__(self, stdscr, height, width, widgets, menus, context):
        self.COLOR_REDBLACK = 1
        self.COLOR_CYAN_BLACK = 2
        self.COLOR_GREEN_BLACK = 3
        self.COLOR_MAGENTA_BLACK = 4
        self.COLOR_BLUE_WHITE = 5
        self.COLOR_YELLOW_BLACK = 6
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_WHITE)
        curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        self.height = height
        self.width = width
        self.widgets = widgets
        self.menus = menus
        self.context = context
        self.stdscr = stdscr
        self.focus_index = 0
        self.title = "This is a data entry form"
        self.title_win = curses.newwin(5, self.width, 0, 0)
        body_height = self.height -  5 - 3 - 3 + 2
        body_start_row = 4
        body_start_col = 0
        self.body_win = curses.newwin(self.height - 5 - 3 - 3 + 2, self.width, 4, 0 )
        self.menu_win = curses.newwin(3, self.width, self.height - 6, 0)
        self.msg_win = curses.newwin(3, self.width, self.height - 4, 0 )
        self.message_text = ""
        body_height = 0
        for w in self.widgets:
            w.win = curses.newwin(1, width + len(w.label) + 2, body_start_row + w.row, body_start_col + w.col, )
            w.form = self
            w.has_focus = False
        for m in self.menus:
            m.form = self
            m.win = self.menu_win

    def msg_error(self, msg):
        label = " ERROR: "
        self.msg_win.clear()
        self.msg_win.addstr(1, 1, label, curses.color_pair(1)+curses.A_STANDOUT )
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

    def handle_menu(self, ch):
        for itm in self.menus:
            if fn_key_match(ch, itm.fn_key):
                itm.invoke(self, self.context)
    
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

    def make_boxes(self):
        # self.stdscr.border(0,0,0,0,0,0,0)
        self.title_win.border(0,0,0,0,0,0,0,0)
        self.body_win.border(0,0,0,0, curses.ACS_LTEE, curses.ACS_RTEE,0,0)
        self.menu_win.border(0,0,0,0, curses.ACS_LTEE, curses.ACS_RTEE, curses.ACS_LTEE, curses.ACS_RTEE)
        self.msg_win.border(0,0,0,0, curses.ACS_LTEE, curses.ACS_RTEE, 0, 0)

    def render_menus(self):
        nbr_menuitems = len(self.menus)
        cols_per_item = (self.width - 2) // nbr_menuitems
        start = 1
        for m in self.menus:
            self.menu_win.move(1,start)
            m.render()
            start += cols_per_item
        self.menu_win.noutrefresh()

    def render_message(self):
        pass
        self.msg_win.addstr(1,1, " Msg: ", curses.color_pair(self.COLOR_MAGENTA_BLACK) + curses.A_BOLD)

    def render(self):
        self.make_boxes()
        self.title_win.addstr(2, (self.width // 2) - (len(self.title) // 2), self.title, curses.A_BOLD + curses.color_pair(self.COLOR_YELLOW_BLACK))
        self.menu_win.addstr(1,1, " Menu: ")
        self.msg_win.addstr(1,1, " Msg: ", curses.color_pair(self.COLOR_MAGENTA_BLACK) + curses.A_BOLD)
        self.title_win.noutrefresh()
        self.body_win.noutrefresh()
        self.menu_win.noutrefresh()
        self.msg_win.noutrefresh()

        for w in self.widgets:
            w.render()

        self.render_menus()
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


def testScreenSize(stdscr):
    h, w = stdscr.getmaxyx()
    if h < requiredHeight or w < requiredWidth:
        raise Exception(
            "SCreen is too small must be at least 15 high and 60 wide")


def menuAction0(context):
    x = context

def menuAction1(context):
    x = context

def menuAction2(context):
    x = context

def menuAction3(context):
    x = context



# def main(stdscr):
#     data = "dummy context"
#     testScreenSize(stdscr)
#     curses.curs_set(2)
#     curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
#     widgets = [ 
#         TextWidget(2,2,"Widget 1st", 20,  "", data),
#         TextWidget(4,2,"Widget 2nd", 20, "", data),
#         TextWidget(6,2,"Widget 3rd", 20, "", data),
#         TextWidget(8,2,"Widget 4th", 20, "", data),
#     ]
#     menus = [ 
#         MenuItem("MFirst", "KEY_FN(1)", menuAction1),
#         MenuItem("MSecond", "KEY_FN(2)", menuAction2),
#         MenuItem("MTHird", "KEY_FN(3)", menuAction3)
#     ]
#     form = Form(stdscr, 20, 100, widgets, menus, data)
#     form.run()

# curses.wrapper(main)


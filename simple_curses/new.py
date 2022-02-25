import time
import sys
import curses
import curses.textpad
import time
import string

menu = ['Home', 'Store Lookup', 'MAC Lookup', 'MAC Clear',
        'Afterhours Wi-Fi Disable/Enable', 'Exit']



requiredHeight = 15
requiredWidth = 60

# 
# A fixed width buffer that can display a window into an arbitory length
# string and handle
#   appending characters
#   backspacing to delete the last character
#   TODO - left and right arrow navigation within the string
#   TODO - deleting an internal character 
# 
class StringBuffer:
    STATE_APPENDING = 1
    STATE_INSERTING = 2
    def __init__(self, str, width):
        self.content = ""
        self.width = width
        self.state = self.STATE_APPENDING
        self.content_position = 0
        self.cursor_position = 0
        self.display_string = ""
        self.start_display_string = 0
        for c in str:
            self.add_ch(c)

    # returns true if the content is larger than the buffer window
    def content_overflow(self):
        tmp = len(self.content) > (self.width - 1)
        return tmp

    # calcs the index position of the cursor in the full content string
    def cursor_pos_in_content(self):
        if len(self.content) == 0 :
            return 0
        else:
            tmp = self.start_display_string + self.cursor_position

    # cursor is over the contents first character
    def cursor_at_content_start(self):
        return self.cursor_pos_in_content() == 0

    # cursor is over the content last character
    def cursor_at_content_end(self):
        return self.cursor_pos_in_content() == len(self.content)

    # cursor is immerdiately to the right of the contents last character 
    def cursor_after_content_end(self):
        return self.cursor_pos_in_content() == len(self.content)
    
    # get a substring of the conttent
    def content_substr(self, start, leng):
        if start == 0 and leng <= 0:
            return ""
        assert (len(self.content) > 0),  "content_substr: content length is zero "
        return self.content[start, start + leng]

    # calcs the string preceeding the cursor
    def prefix(self):
        if(len(self.content) == 0):
            return ""
        if self.cursor_position == 0:
            return ""
        if(len(self.content) <= self.width - 1):
            tmp = self.content[0: self.cursor_position - 1]
            return tmp

        tmp = self.content[self.start_display_string, self.start_display_string + self.width - 1 ]
        return tmp

    # calcs the string after the cursor position
    def suffix(self):
        if(len(self.content) == 0):
            return ""
        if self.cursor_position == self.width - 1:
            return ""
        pass


    def add_ch(self, ch):
        
        if self.state == self.STATE_APPENDING:
            if len(self.content) <= (self.width - 2):
                self.content += ch
                self.display_string = self.content + " "
                self.start_display_string = 0
                self.cursor_position = len(self.content) 
            else:
                self.content += ch
                self.start_display_string = len(self.content) - (self.width - 1)
                self.display_string = self.content[len(self.content) - (self.width - 1): len(self.content)] + " "
                self.cursor_position = self.width - 1

    #delete the character to the left of the cursor
    def back_space(self):
        if self.state == self.STATE_APPENDING:
            if len(self.content) <= (self.width - 1):
                self.content = self.content[0: len(self.content) - 1]
                self.start_display_string = 0
                self.display_string = self.content + " "
                self.cursor_position = len(self.content) 
            else:
                self.content = self.content[0: len(self.content) - 1]
                self.start_display_string = len(self.content) - (self.width - 1)
                self.display_string = self.content[len(self.content) - (self.width - 1): len(self.content)] + " "
                self.cursor_position = self.width - 1

    # delete the character under the cursor
    def delete(self):
        if (self.cursor_position == self.width - 1) and (self.start_display_string + self.width) == len(self.content):
            pass
        else
            prefix = self.content[0: self.cursor_position + self.start_display_string - 1]
            suffix = self.content[self.cursor_position + self.start_display_string ]
        pass

    def left(self):
        if self.cursor_position > 0 and self.cursor_position <= self.width - 1:
            self.cursor_position -= 1
        elif self.cursor_position == 0:
            if self.start_display_string > 0:
                self.start_display_string -= 1
                end = self.start_display_string + self.width - 1
                self.display_string = self.content[self.start_display_string : end] + " "
            else:
                pass
        else:
            pass

    def right(self):
        if self.cursor_position >= 0 and self.cursor_position < (self.width - 1):
            self.cursor_position += 1
        elif self.cursor_position == self.width - 1:
            # if self.start_display_string + self.width - 1 == len(self.content): # cannot move right any further
            #     pass
            if self.start_display_string < len(self.content) - 1 and (self.start_display_string + self.width - 1 != len(self.content)): # can move right
                self.start_display_string += 1 
                end = self.start_display_string + self.width - 1
                self.display_string = self.content[self.start_display_string : end] + " "
            else:
                pass
        else:
            pass

# 
# tests an input string to see if it represents an editing character
# 
def is_edit_character(ch):
    pass
def is_edit_back(ch):
    return (len(ch) == 1) and (ch[0] == 0x7f)

def is_edit_del(ch):
    return (ch == "KEY_DC")

def is_edit_move_back(ch):
    return (ch == "KEY_DC")

def is_edit_move_forward(ch):
    return (ch == "KEY_DC")


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
        self.attributes = attributes
        self.form = None
        tmp = width + len(self.label)
        self.win = curses.newwin(1, width + len(self.label), row, col, )
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
            self.win.addstr(0, i, "Z", curses.A_REVERSE)
    # 
    # calculate the portion of self.content that can be displayed in the
    # text widgets curses window.
    # THe portion has length <= width - 1 leaving space for the cursor at the end
    # 
    def displayable_content(self):
        if (len(self.content) <= (self.width - 1)) and (self.display_content_position == len(self.content)):
            # this is the case where the content fits in the window with room for a cursor at the end
            self.display_content_start = 0
            self.display_cursor_position = len(self.content)
            self.display_length = len(self.content) + 1
            return self.content + " "
        elif (len(self.content) <= (self.width - 1)) and (self.display_content_position < len(self.content)) :
            # this is situation where content fits in the wiindow but the cursor is not after end of string 
            self.display_content_start = 0
            self.display_cursor_position = self.display_content_position
            return self.content
        elif (len(self.content) >= self.width):
            # this is situation where content fits in the wiindow but the cursor is not after end of string 
            self.display_content_start = len(self.content) - (self.width - 1)
            self.display_cursor_position = self.display_content_position
            return self.content
        else:
            pass
    # called by the containing form to paint/render the Widget
    def render(self):
        self.paint_content_area_background()
        self.win.addstr(0, 0, self.label)
        self.win.addstr(0, len(self.label), self.displayable_content())
        if self.has_focus:
            self.position_cursor()
        self.win.noutrefresh()
    
    # 
    # Positions the cursor to the current active position and makes sure it blinks.
    # The current active position is usually 1 space past the end of the currently input text
    # 
    def position_cursor(self):
        out_str = self.label + self.content
        cpos = self.content_position
        self.win.addnstr(0, len(out_str), "Y", 1, curses.A_REVERSE + curses.A_BLINK)
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
            self.content += ch
            self.content_position += 1
            # self.win.addstr(0, 1 + len(self.label) + len(self.content), self.content)
        elif is_edit_back(ch):
            # not at beginning ?
            if self.content_position > 0:
                self.content_position -= 1
                self.content = self.content[0: len(self.content)-1]
            else:
                self.invalid_input()
        elif is_edit_del(ch):
            # not at end
            if self.content_position < (len(self.content) - 1):
                self.content = self.content[0:self.content_position] + self.content[self.content_position+1]
            else:
                self.invalid_input()
        elif is_edit_move_back(ch):
            if self.content_position > 0:
                self.content_position -= 1
            else:
                self.invalid_input()
        elif is_edit_move_forward(ch):
            if self.content_position < (len(self.content) - 1):
                self.content_position += 1
            else:
                self.invalid_input()
        else:
            did_handle_ch = False

        self.position_cursor()
        return did_handle_ch

def is_next_control(ch):
    return (ch == "KEY_RIGHT")

def is_prev_control(ch):
    return (ch == "KEY_LEFT")

def is_function_key(ch):
    return (ch[0:6] == "KEY_FN(")

def fn_key_match(k1, k2):
    return (k1 == k2)

def fn_key_description(k1):
    s1 = k1.replace("KEY_FN(", "")
    s2 = s1.replace(")", "")
    s3 = "F"+s2
    return s3

class MenuItem:
    def __init__(self, name, fn_key, function):
        self.name = name
        self.fn_key = fn_key
        self.function = function
        self.form = None

    def invoke(self, fn_key, context):
        self.function(context)
    
    def render(self):
        pass

class Form:
    def __init__(self, stdscr, height, width, widgets, menus, context):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.height = height
        self.width = width
        self.widgets = widgets
        self.menus = menus
        self.context = context
        self.stdscr = stdscr
        self.focus_index = 0
        self.title = "This is a data entry form"
        self.title_win = curses.newwin(5, self.width, 0, 0)
        self.body_win = curses.newwin(self.height - 5 - 3 - 3 + 2, self.width, 4, 0 )
        self.menu_win = curses.newwin(3, self.width, self.height - 6, 0)
        self.msg_win = curses.newwin(3, self.width, self.height - 4, 0 )
        for w in self.widgets:
            w.form = self
            w.has_focus = False
        for m in self.menus:
            m.form = self

    def msg_error(self, msg):
        label = " ERROR: "
        self.msg_win.addstr(1, 1, label, curses.color_pair(1)+curses.A_STANDOUT )
        self.msg_win.addstr(1, 1 + len(label), msg)
        self.msg_win.noutrefresh()
        curses.doupdate()

    def msg_warn(self, msg):
        label = " WARNING: "
        self.msg_win.addstr(1, 1, label )
        self.msg_error.addstr(1, 1 + len(label), msg)
        self.msg_win.noutrefresh()
        curses.doupdate()

    def msg_info(self, msg):
        label = " INFO: "
        self.msg_win.addstr(1, 1 , label )
        self.msg_error.addstr(1, 1 + len(label), msg)
        self.msg_win.noutrefresh()
        curses.doupdate()

    def handle_menu(self, ch):
        for itm in self.menu:
            if fn_key_match(ch, itm.fn_key):
                itm.invoke()
    
    def handle_input(self):
        # here should render everything to ensure the latest version of the screen is being seen
        # hen input is provided
        ch = self.stdscr.getkey()
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
        self.title_win.border(0,0,0,0,0,0,0)
        self.body_win.border(0,0,0,0,0,0,0)
        self.menu_win.border(0,0,0,0, curses.ACS_LTEE, curses.ACS_RTEE, curses.ACS_LTEE, curses.ACS_RTEE)
        self.msg_win.border(0,0,0,0, curses.ACS_LTEE, curses.ACS_RTEE, 0, 0)

    def render(self):
        self.make_boxes()
        self.title_win.addstr(2, (self.width // 2) - (len(self.title) // 2), self.title)
        self.menu_win.addstr(1,1, " Menu: ")
        self.msg_win.addstr(1,1, " Msg: ")
        self.title_win.noutrefresh()
        self.body_win.noutrefresh()
        self.menu_win.noutrefresh()
        self.msg_win.noutrefresh()

        for w in self.widgets:
            w.render()

        menu_string = "  "
        for m in self.menus:
            menu_string +=fn_key_description(m.fn_key) + "-" + m.name + "  " 

        self.menu_win.addstr(1,1,menu_string)
        self.menu_win.noutrefresh()

        curses.doupdate()
        # self.stdscr.refresh()

    def run(self):
        self.widgets[self.focus_index].focus_accept()
        self.render()
        time.sleep(5)
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

def test_add_back():
    sb = StringBuffer("", 5)
    print(sb.display_string, sb.cursor_position)
    sb.add_ch("a")
    print(sb.display_string, sb.cursor_position)

    sb.add_ch("b")
    print(sb.display_string, sb.cursor_position)
    sb.add_ch("c")
    print(sb.display_string, sb.cursor_position)

    sb.add_ch("d")
    print(sb.display_string, sb.cursor_position)
    sb.add_ch("e")
    print(sb.display_string, sb.cursor_position)
    sb.add_ch("f")    
    print(sb.display_string, sb.cursor_position)

    sb.add_ch("g")    
    print(sb.display_string, sb.cursor_position)
    sb.add_ch("h")    
    print(sb.display_string, sb.cursor_position)
    sb.back_space()    
    print(sb.display_string, sb.cursor_position)
    sb.back_space()    
    print(sb.display_string, sb.cursor_position)
    sb.back_space()    
    print(sb.display_string, sb.cursor_position)
    sb.back_space()    
    print(sb.display_string, sb.cursor_position)
    sb.back_space()    
    print(sb.display_string, sb.cursor_position)
    sb.back_space()    
    print(sb.display_string, sb.cursor_position)

def test_left_right_01():
    sb = StringBuffer("abc", 5)
    print(sb.display_string, sb.cursor_position)
    sb.left()
    print(sb.display_string, sb.cursor_position)
    sb.right()
    print(sb.display_string, sb.cursor_position)
    sb.left()
    print(sb.display_string, sb.cursor_position)
    sb.left()
    print(sb.display_string, sb.cursor_position)
    sb.right()
    print(sb.display_string, sb.cursor_position)
    sb.right()
    print(sb.display_string, sb.cursor_position)


def test_left_01():
    sb = StringBuffer("abcdefg", 5)
    print(sb.display_string, sb.cursor_position)
    sb.left()
    print(sb.display_string, sb.cursor_position)
    sb.left()
    print(sb.display_string, sb.cursor_position)
    sb.left()
    print(sb.display_string, sb.cursor_position)
    sb.left()
    print(sb.display_string, sb.cursor_position)
    sb.left()
    print(sb.display_string, sb.cursor_position)
    sb.left()
    print(sb.display_string, sb.cursor_position)
    sb.left()
    print(sb.display_string, sb.cursor_position)
    sb.left()
    print(sb.display_string, sb.cursor_position)

def test_right_01():
    sb = StringBuffer("abcdefg", 5)
    print(sb.display_string, sb.cursor_position)
    sb.left()
    sb.left()
    sb.left()
    sb.left()
    sb.left()
    sb.left()
    sb.left()
    sb.left()
    print(sb.display_string, sb.cursor_position)
    sb.right()
    print(sb.display_string, sb.cursor_position)
    sb.right()
    print(sb.display_string, sb.cursor_position)
    sb.right()
    print(sb.display_string, sb.cursor_position)
    sb.right()
    print(sb.display_string, sb.cursor_position)
    sb.right()
    print(sb.display_string, sb.cursor_position)
    sb.right()
    print(sb.display_string, sb.cursor_position)
    sb.right()
    print(sb.display_string, sb.cursor_position)
    sb.right()
    print(sb.display_string, sb.cursor_position)
    sb.right()
    print(sb.display_string, sb.cursor_position)
    sb.right()
    print(sb.display_string, sb.cursor_position)
    sb.right()
    print(sb.display_string, sb.cursor_position)



if __name__ == '__main__':
    # test_add_back()
    # test_left_right_01()
    test_left_01()
    # test_right_01()
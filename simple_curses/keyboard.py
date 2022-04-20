import curses
import curses.textpad
import string
"""
This file implements the mapping from keycodes to actions
"""
getch_flag = True


def get_character(stdscr):
    ch = None
    if getch_flag:
        ch = stdscr.getch()
    else:
        ch = stdscr.getkey()

# keys for moving between views
def is_control_v(ch):
    return ch == 0x16


# tabbing keys between fields in a view
def is_next_control(ch):
    return ch == 0x09 #tab


def is_prev_control(ch):
    return ch == 0x161 #shift tab


#function keys
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


# tests if a key re presents a printable character
def is_printable(chint):
    if chint > 255:
        return False
    ch = chr(chint)
    # printable but not tab of shift tab
    return (ch in string.printable) and (chint != 0x09) and (chint != 0x161)

#
# editing keys
# 
def is_addline(ch):
    return False


def is_cntrl_p(ch):
    return ch == 0x10


def is_edit_back(ch):
    """test ch is backspace"""
    return ch == 0x7f or ch == 0x107

def is_edit_character(ch):
    pass


def is_edit_del(ch):
    """the delete key"""
    return ch == curses.KEY_DC

def is_return(chint):
    if chint > 255:
        return False
    ch = chr(chint)
    return ch == '\r'


def is_linefeed(chint):
    if chint > 255:
        return False
    ch = chr(chint)
    return ch == '\n'


def is_space(chint):
    if chint > 255:
        return False
    ch = chr(chint)
    return ch == " "


def is_newline(chint):
    if chint > 255:
        return False
    ch = chr(chint)
    return ch == '\n'

def is_delete_line(ch):
    return False


# movement within a widget field
def is_move_left(ch):
    return ch == curses.KEY_SLEFT or ch == curses.KEY_LEFT


def is_move_right(ch):
    return ch == curses.KEY_SRIGHT  or ch == curses.KEY_RIGHT


def is_move_down(ch):
    return ch == curses.KEY_DOWN


def is_move_up(ch):
    return ch == curses.KEY_UP


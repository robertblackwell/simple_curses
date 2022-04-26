import curses
import curses.textpad
import string
"""
This file implements the mapping from keycodes to actions
"""
getch_flag = True

FKEY_F1 = curses.KEY_F1
FKEY_F2 = curses.KEY_F2
FKEY_F3 = curses.KEY_F3
FKEY_F4 = curses.KEY_F4
FKEY_F5 = curses.KEY_F5
FKEY_F6 = curses.KEY_F6
FKEY_F7 = curses.KEY_F7
FKEY_F8 = curses.KEY_F8
# FKEY_F9 = curses.KEY_F9
# FKEY_F10 = curses.KEY_F10
# FKEY_F11 = curses.KEY_F11
# FKEY_F12 = curses.KEY_F12

FKEY_SHIFT_F1 = curses.KEY_F13
FKEY_SHIFT_F2 = curses.KEY_F14
FKEY_SHIFT_F3 = curses.KEY_F15
FKEY_SHIFT_F4 = curses.KEY_F16
FKEY_SHIFT_F5 = curses.KEY_F17
FKEY_SHIFT_F6 = curses.KEY_F18
FKEY_SHIFT_F7 = curses.KEY_F19
FKEY_SHIFT_F8 = curses.KEY_F20
# FKEY_SHIFTF_9 = curses.KEY_F9
# FKEY_SHIFTF_10 = curses.KEY_F10
# FKEY_SHIFTF_11 = curses.KEY_F11
# FKEY_SHIFTF_12 = curses.KEY_F12

FKEY_CTRL_F1 = curses.KEY_F25
FKEY_CTRL_F2 = curses.KEY_F26
FKEY_CTRL_F3 = curses.KEY_F27
FKEY_CTRL_F4 = curses.KEY_F28
FKEY_CTRL_F5 = curses.KEY_F29
FKEY_CTRL_F6 = curses.KEY_F30
FKEY_CTRL_F7 = curses.KEY_F31
FKEY_CTRL_F8 = curses.KEY_F32
# FKEY_CTRLF_9 = curses.KEY_F9
# FKEY_CTRLF_10 = curses.KEY_F10
# FKEY_CTRLF_11 = curses.KEY_F11
# FKEY_CTRLF_12 = curses.KEY_F12


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

def function_key_ord(key):
    return key - curses.KEY_F0

def function_key_number(key):
    if curses.KEY_F0 <= key <= curses.KEY_F12:
        n = key - curses.KEY_F0
    elif curses.KEY_F12 <= key <= curses.KEY_F24:
        n = key - curses.KEY_F12
    elif curses.KEY_F24 <= key <= curses.KEY_F36:
        n = key - curses.KEY_F24
    else:
        n = None
    return n

def function_key_description(key):
    if curses.KEY_F0 <= key <= curses.KEY_F12:
        prefix = "F"
    elif curses.KEY_F13 <= key <= curses.KEY_F24:
        prefix = "SF"
    elif curses.KEY_F25 <= key <= curses.KEY_F36:
        prefix = "^F"
    else:
        prefix = "??"
    s = "{}{}".format(prefix, function_key_number(key))
    return s


class FunctionKeys:
    def __init__(self):
        self.accelerators = {}

    def test_duplicate_error(self, key):
        if key in self.accelerators:
            msg = "Function key [{}, {}] is already being used.".format(key, function_key_description(key))
            raise ValueError("Duplicate function key. {}  ".format(msg))

    def add_accelerator(self, key, menu):
        self.test_duplicate_error(key)
        self.accelerators[key] = menu

    def get_menu(self, key):
        if key in self.accelerators:
            return self.accelerators[key]
        return None

    def is_function_key(self, key):
        return curses.KEY_F0 <= key <= curses.KEY_F36

    def description(self, key):
        return function_key_description(key)

if __name__ == "__main__":
    fkeys = [ 
        (curses.KEY_F0, "FK_0"),
        (curses.KEY_F1, "FK_1"),
        (curses.KEY_F2, "FK_2"),
        (curses.KEY_F3, "FK_3"),
        (curses.KEY_F4, "FK_4"),
        (curses.KEY_F5, "FK_5"),
        (curses.KEY_F6, "FK_6"),
        (curses.KEY_F7, "FK_7"),
        (curses.KEY_F8, "FK_8"),
        (curses.KEY_F9, "FK_9"),
        (curses.KEY_F10,"FK_10"),
        (curses.KEY_F11,"FK_11"),
        (curses.KEY_F12,"FK_12"),
        (curses.KEY_F13,"FK_13"), #also Shift F1
        (curses.KEY_F14,"FK_14"),
        (curses.KEY_F15,"FK_15"),
        (curses.KEY_F16,"FK_16"),
        (curses.KEY_F17,"FK_17"),
        (curses.KEY_F18,"FK_18"),
        (curses.KEY_F19,"FK_19"),
        (curses.KEY_F20,"FK_20"),
        (curses.KEY_F21,"FK_21"),
        (curses.KEY_F22,"FK_22"),
        (curses.KEY_F23,"FK_23"),
        (curses.KEY_F24,"FK_24"),# also shift F12
        (curses.KEY_F25,"FK_25"),# also cntrl F1
        (curses.KEY_F26,"FK_26"),
        (curses.KEY_F27,"FK_27"),
        (curses.KEY_F28,"FK_28"),
        (curses.KEY_F29,"FK_29"),
        (curses.KEY_F30,"FK_30"),
        (curses.KEY_F31,"FK_31"),
        (curses.KEY_F32,"FK_32"),
        (curses.KEY_F33,"FK_33"),
        (curses.KEY_F34,"FK_34"),
        (curses.KEY_F35,"FK_35"),
        (curses.KEY_F36,"FK_36"),
        (curses.KEY_F37,"FK_37"),# else cnttrl F12
    ]
    fk = FunctionKeys()
    b1 = fk.is_function_key(curses.KEY_F1)
    b2 = fk.is_function_key(curses.KEY_F13)    
    b3 = fk.is_function_key(curses.KEY_F25)
    s1 = fk.description(curses.KEY_F1)
    s2 = fk.description(curses.KEY_F13)    
    s3 = fk.description(curses.KEY_F25)
    numbers = []
    for i in range(0,37):
        k = curses.KEY_F0 + i
        numbers.append((function_key_description(k), k, function_key_number(k), fkeys[i]))
    n1 = function_key_number(curses.KEY_F1)
    n12 = function_key_number(curses.KEY_F12)
    n2 = function_key_number(curses.KEY_F13)
    n22 = function_key_number(curses.KEY_F24)
    n3 = function_key_number(curses.KEY_F25)    
    n32 = function_key_number(curses.KEY_F35)

    print("hello")
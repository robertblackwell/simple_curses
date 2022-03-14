import time
import sys
from abc import ABC, abstractmethod, abstractproperty
import curses
import curses.textpad
import time
import string

import string_buffer
import lines_buffer
from colors import Colors
import validator

getch_flag = True
def get_character(stdscr):
    ch = None
    if getch_flag:
        ch = stdscr.getch()
    else:
        ch = stdscr.getkey()
# 
# tests an input string to see if it represents an editing character
# 
def is_addline(ch):
    return False
def is_cntrl_p(ch):
    return (ch == 0x10)
        
def is_edit_character(ch):
    pass

def is_printable(chint):
    if chint > 255:
        return False
    ch = chr(chint)
    return ch in string.printable


def is_edit_back(ch):
    """test ch is backspace"""
    return (ch == 0x7f)

def is_edit_del(ch):
    return ch == curses.KEY_DC

def is_move_left(ch):
    return (ch == curses.KEY_SLEFT)

def is_move_right(ch):
    return (ch == curses.KEY_SRIGHT)

def is_move_down(ch):
    return (ch == curses.KEY_DOWN)

def is_move_up(ch):
    return (ch == curses.KEY_UP)

def is_next_control(ch):
    return (ch == curses.KEY_RIGHT)

def is_prev_control(ch):
    return (ch == curses.KEY_LEFT)

def is_function_key(ch):
    assert False
    tmp = ch[0:6]
    return (tmp == "KEY_F(")

def fn_key_match(k1, k2):
    return (k1 == k2)

def fn_key_description(k1):
    assert False
    s1 = k1.replace("KEY_F(", "")
    s2 = s1.replace(")", "")
    s3 = "F"+s2
    return s3


def is_return(chint):
    if chint > 255:
         return False
    ch = chr(chint)
    return (ch == '\r')

def is_linefeed(chint):
    if chint > 255:
         return False
    ch = chr(chint)
    return (ch == '\n')

def is_space(chint):
    if chint > 255:
         return False
    ch = chr(chint)
    return (ch == " ")

def is_newline(chint):
    if chint > 255:
         return False
    ch = chr(chint)
    return (ch == '\n')

def is_delete_line(ch):
    return False

class Keyboard:
    _instance = None
    def __init__(self):
        raise RuntimeError('Call instance() instead')
    @classmethod
    def instance(cls):
        if cls._instance is None:
            if getch_flag:
                cls._instance = Keyboard_getch(curses.stdscr)
            else:
                cls._instance = Keyboard_getkey(curses.stdscr)
        
        return cls._instance


class Keyboard_getch:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        pass
class Keyboard_getkey:
    def __init__(self):
        self.stdscr = stdscr
        pass
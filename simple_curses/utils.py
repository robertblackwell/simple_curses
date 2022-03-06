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


# 
# tests an input string to see if it represents an editing character
# 
def is_addline(ch):
    return False
def is_cntrl_p(ch):
    return (ch == "\x10")
        
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

def is_move_down(ch):
    return (ch == "KEY_DOWN")

def is_move_up(ch):
    return (ch == "KEY_UP")

def is_return(ch):
    return (ch == '\r')

def is_linefeed(ch):
    return (ch == '\n')

def is_space(ch):
    return (ch == " ")

def is_newline(ch):
    return (ch == '\n')

def is_delete_line(ch):
    return False


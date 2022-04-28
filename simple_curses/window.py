import curses
from simple_curses.kurses_ex import *

def newwin_inside(hostwin, h, w, y, x):
    """
    Create a new curses window that is fully inside the host window
    :param hostwin : curses.win
    :param h : non neg int      Height of new window
    :param w : non neg int      Width of new window
    :param y : starting row of new window within host window (relative)
    :param x : starting column of new window within host (relative) 
    """
    ybeg, xbeg = hostwin.getbegyx()
    ymax, xmax = hostwin.getmaxyx()
    win = curses.newwin(h, w, ybeg + y, xbeg + x)
    return win

def newwin_after(prev_win, h, w, xstart, y_skip=1):
    """
    Create a new curses window starting:
    -   on the y_skip rows after the prev_win,
    -   starting at absolute column xstart

    :param prev_win : curses.win
    :param h : non neg int      Height of new window
    :param w : non neg int      Width of new window
    :param y : starting row of new window within host window (relative)
    :param x : starting column of new window within host (relative) 
    """
    ybeg, xbeg = prev_win.getbegyx()
    ymax, xmax = prev_win.getmaxyx()
    win = curses.newwin(h, w, ybeg + ymax + y_skip - 1, xstart)
    return win
def hline_after(prev_win, xstart=0):
    """
    Create a new window on the next row after prev_win.
    The new window will be for a horizontal line and hence
    only needs to be 1 line high.
    To underline the previous window it is 2 cols wider than the pre_win
    :param prev_win: curses.win
    :param xstart : non neg int The starting absolute column for the hline, usually 1 less than prev_win.xbeg 
    """
    ybeg, xbeg = prev_win.getbegyx()
    ymax, xmax = prev_win.getmaxyx()
    win = curses.newwin(1, xmax+2, ybeg + ymax, xstart)
    return win

def draw_hline(win):
    """
    Draw a horizontal line startiing at position 0,0 in win and 
    as wide as win
    """
    win.border(0, 0, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_LTEE, curses.ACS_RTEE, curses.ACS_LTEE, curses.ACS_RTEE)

class Window:
    @staticmethod
    def mainwin():
        pass
    def newwin(nbr_rows, nbr_cols, ybeg_abs, xbeg_abs):
        ymax, xmax = curses.stdscr.getbegyx()
        if nbr_rows > ymax or nbr_cols > xmax:
            raise ValueError("Window is bigger than stdscr")
        cwin = curses.newwin(nbr_rows, nbr_cols, ybeg_abs, xbeg_abs)
        w = Window(cwin)
        w.parent = curses.stdscr
        return w

    """Wrapper for curses.win in order to provide more diagnostics and a single bug fix"""
    def __init__(self, cwin, nbr_rows, nbr_cols, ybeg_abs, xbeg_abs):
        ymax, xmax = curses.stdscr.getbegyx()
        if nbr_rows > ymax or nbr_cols > xmax:
            raise ValueError("Window is bigger than stdscr")
        self.xbeg = xbeg_abs
        self.ybeg = ybeg_abs
        self.ymax = nbr_rows
        self.xmax = nbr_cols
        self.parent = None
        self.children = []
        self.cwin = cwin

    def subwin(self, nbr_lines, nbr_cols, ybeg_rel, xbeg_rel):
        neww = make_subwin(self.cwin, nbr_lines, nbr_cols, ybeg_rel, xbeg_rel)
        csubwin = Window(csubwin, nbr_lines, nbr_cols, ybeg_rel, xbeg_rel)
        csubwin.parent = self
        return csubwin
import curses

# 
# Module which holds local extensions to curses
# 
def make_subwin(win, nbr_rows: int, nbr_cols: int, y_begin_relative: int, x_begin_relative: int): 
    """
    A slightly safer way of making a curses subwin - it checks that start and end points are inside the parent window

    Parameters
    ----------
        win     
            parent window - the subwindow must be entirely within the parent window
        nbr_rows: int          
            number of rows in sub window
        nbr_cols: int          
            number of columns in sub window
        y_begin_relative: int  
            starting row relative to parent window 
        x_begin_relative: int  
            starting column relative to parent window

    Returns
    -------
        curses.window a subwindow of win

    Raises
    ------
        assert error if the start or end points of the proposed subwin are not inside the parent window
    """
    yb, xb = win.getbegyx()
    ym, xm = win.getmaxyx()
    y_begin_abs = y_begin_relative + yb
    x_begin_abs = x_begin_relative + xb
    if not (yb <= y_begin_abs <= yb + ym) :
        raise ValueError("yb: {} y_begin_abs: {} yb + ym:{}".format(yb, y_begin_abs, yb+ym))
    if not (xb <= x_begin_abs <= xb + xm):
        raise ValueError("xb: {} x_begin_abs: {} xb + xm:{}".format(xb, x_begin_abs, xb+xm))
    if not (yb <= y_begin_abs + nbr_rows <= yb + ym):
        raise ValueError("yb: {} y_begin_abs + nbr_rows: {} yb + ym:{}".format(yb, y_begin_abs + nbr_rows, yb+ym))
    if not (xb <= x_begin_abs + nbr_cols <= xb + xm):
        raise ValueError("xb: {} x_begin_abs + nbr_cols: {} xb + xm:{}".format(xb, x_begin_abs+nbr_cols, xb+xm))
    sw = win.subwin(nbr_rows, nbr_cols, y_begin_abs, x_begin_abs)
    return sw

def win_addstr(win, y, x, astring, attr=0):
    """
    A wrapper for curses addstr that provides more diagnostic info for running off the edge of a window.
    and to fix the bug in the curses module that will not let the provided addstr with the bottom right
    hand character to a curses.win or curses.win.subwin
    """
    ybeg, xbeg = win.getbegyx()
    ymax, xmax = win.getmaxyx()
    length = len(astring)
    if y > ymax - 1 or x + length > xmax:
        raise ValueError("string {} (length={}) is too big to fit in window of size ({}x{}) at position({},{}))".format(s, len(s), ymax, xmax ,y ,x))
    
    bottom_right_position_flag = y == ymax - 1 and x + length == xmax
    if bottom_right_position_flag:
        try:
            win.addstr(y, x, astring)
        except curses.error:
            pass
    else:
        win.addstr(y, x, astring)

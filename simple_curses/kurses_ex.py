import curses

# 
# Module which holds local extensions to curses
# 
def make_subwin(win: curses.window, nbr_rows: int, nbr_cols: int, y_begin_relative: int, x_begin_relative: int): 
    """
    A slightly safer way of making a curses subwin - it checks that start and end points are inside the parent window

    Parameters
    ----------
        win: curses.window     
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


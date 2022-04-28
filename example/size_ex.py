import curses
from linecache import lazycache

def subwin_relative(win, row_count, col_count, relative_begin_y, relative_begin_x):
    win_top_left_abs = win.getbegyx()
    p = win.getparyx()
    max = win.getmaxyx()
    max_y = max[0]
    max_x = max[1]
    abs_y = win_top_left_abs[0] + relative_begin_y
    abs_x = win_top_left_abs[1] + relative_begin_x 

    swin = win.subwin(row_count, col_count, abs_y, abs_x)
    return swin

def addstr_middle(win, y, str, attr):
    beg = win.getparyx()
    siz = win.getmaxyx()
    w = siz[1] - beg[1]
    tcol = (w - len(str)) // 2
    win.addstr(y, tcol, str, attr)

def safe_addstr(win, y, x, s, attr=0):
    ybeg, xbeg = win.getbegyx()
    ymax, xmax = win.getmaxyx()
    length = len(s)
    if y > ymax - 1 or x + length > xmax:
        raise ValueError("string {} (length={}) is too big to fit in window of size ({}x{}) at position({},{}))".format(s, len(s), ymax, xmax ,y ,x))
    
    bottom_right_position_flag = y == ymax - 1 and x + length == xmax
    if bottom_right_position_flag:
        try:
            win.addstr(y, x, s, attr)
        except curses.error:
            pass
    else:
        win.addstr(y, x, s, attr)

def main(stdscr):
    curses.curs_set(2)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_YELLOW)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.curs_set(0)

    h, w = stdscr.getmaxyx()
    h = h
    w = w
    stdscr.bkgd(" ", curses.color_pair(5))
    outter_win = curses.newwin(60, 120, 2, 2)
    outter_win.bkgd(" ", curses.color_pair(4))
    mwin = subwin_relative(outter_win, 2, 20, 0 , 0)
    mwin.bkgd(" ", curses.color_pair(1))
    # this works because it soes not try and fill the last character spot
    try:
        safe_addstr(mwin, 0, 0, "123456789A123456789B")
    except:
        pass
    # this fails because it fillws the last character spot

    try:
        safe_addstr(mwin, 1, 0, "123456789A123456789B")
    except curses.error as e:
        report = "{}".format(e)
        pass
    stdscr.noutrefresh()
    mwin.noutrefresh()
    curses.doupdate()


    ch = " "
    while ch != "q":
        ch = stdscr.getkey()

curses.wrapper(main)


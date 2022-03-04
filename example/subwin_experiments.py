import curses

from numpy import inner


def subwin_relative(win, row_count, col_count, relative_begin_y, relative_begin_x):
    parent_top_left = win.getbegyx()
    parent_max = win.getmaxyx()
    p_max_y = parent_max[0]
    p_max_x = parent_max[1]
    if row_count + relative_begin_y > p_max_y:
        raise RuntimeError("subwin_relative - y values exceed parent boundaries")
    if col_count + relative_begin_x > p_max_x:
        raise RuntimeError("subwin_relative - x values exceed parent boundaries")

    abs_y = parent_top_left[0] + relative_begin_y
    abs_x = parent_top_left[1] + relative_begin_x 
    swin = win.subwin(row_count, col_count, abs_y, abs_x)
    return swin

def addstr_middle(win, y, str, attr):
    beg = win.getparyx()
    siz = win.getmaxyx()
    w = siz[1] - beg[1]
    tcol = (w - len(str)) // 2
    win.addstr(y, tcol, str, attr)

class Form2:
    def __init__(self, stdscr, widgets, context):
        mx = stdscr.getmaxyx()
        h = mx[0] - 2
        w = mx[1] - 2
        stdscr.bkgd(" ", curses.color_pair(5))
        self.height = height
        self.width = width
        self.widgets = widgets
        self.context = context
        self.stdscr = stdscr
        self.focus_index = 0
        self.title = "This is a data entry form"

        self.title_start_row = 0
        self.title_start_col = 0
        self.title_height = 5
        self.title_width = self.width
        self.outter_win = stdscr.subwin(self.height + 2, self.width + 2, 0, 0)
        self.inner_win = self.outter_win.subwin(self.height, self.width, 1, 1)
        self.title_win = curses.newwin(self.title_height, self.title_width, 0, 0)


def main(stdscr):
    curses.curs_set(2)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_YELLOW)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_WHITE)

    mx = stdscr.getmaxyx()
    h = mx[0] - 2
    w = mx[1] - 2
    stdscr.bkgd(" ", curses.color_pair(5))
    # outter_win = curses.newwin(60, 120, 2, 2)
    # mwin = stdscr.subwin(h + 2, w + 2, 0, 0)
    mwin = subwin_relative(stdscr, h + 2, w + 2, 0 , 0)
    mwin.bkgd(" ", curses.color_pair(1))
    mwin_pos = mwin.getparyx()
    mwin_begin = mwin.getbegyx()
    mwin_max = mwin.getmaxyx()
    mwin.addstr(50, 0, "getparyx r: {} c: {}".format(mwin_pos[0], mwin_pos[1]))
    mwin.addstr(51, 0, "getbeginyx r: {} c: {}".format(mwin_begin[0], mwin_begin[1]))
    mwin.addstr(51, 0, "getmaxyx r: {} c: {}".format(mwin_max[0], mwin_max[1]))

    def innerf(y, x):
        # inner_win = mwin.subwin(h, w, 1, 1)
        inner_win = subwin_relative(mwin, h, w, 1, 1)
        inner_win.bkgd(" ", curses.color_pair(1))
        inner_win_pos = inner_win.getparyx()
        inner_win_beg = inner_win.getbegyx()
        inner_win_max = inner_win.getmaxyx()
        inner_win.addstr(1, 0, "inner_win getparyx r: {} c: {}".format(inner_win_pos[0], inner_win_pos[1]))
        inner_win.addstr(2, 0, "inner_win getbegyx r: {} c: {}".format(inner_win_beg[0], inner_win_beg[1]))
        inner_win.addstr(3, 0, "inner_win getmaxyx r: {} c: {}".format(inner_win_max[0], inner_win_max[1]))
        return inner_win
    

    def twinf(stdscr, inner_win, y, x):
        twin = subwin_relative(inner_win, 22, 70, y, x)
        twin.bkgd(" ", curses.color_pair(3))
        twin_pos = twin.getparyx()
        twin_beg = twin.getbegyx()
        twin_max = twin.getmaxyx()
        twin.addstr(3, 0, "twin getparyx r: {} c: {}".format(twin_pos[0], twin_pos[1]))
        twin.addstr(4, 0, "twin getbegyx r: {} c: {}".format(twin_beg[0], twin_beg[1]))
        twin.addstr(5, 0, "twin getmaxyx r: {} c: {}".format(twin_max[0], twin_max[1]))
        twin.addstr(6, 0, "twin = subwin_relative(mwin, 22, 70, {}, {})".format(y, x))
        inner_win.addstr(twin_beg[0], twin_beg[1], "X - getbegyx() relative to inner_win - WRONG")
        stdscr.addstr(twin_beg[0], twin_beg[1], "Y - getbegyx() relative to stdscr - CORRECT")
        stdscr.addstr(twin_pos[0], twin_pos[1], "Z - getparyx() relative to stdscr - INCORRECT")

        for i in range(0, twin_max[0]):
            twin.addstr(i, 45, "Y{}".format(i))
        for i in range(0, twin_max[1]):
            twin.addstr(17, i, "{}".format(i // 10))
            twin.addstr(18, i, "{}".format(i % 10))
        return twin

    def twinf2(stdscr, inner_win, y, x):
        twin = subwin_relative(inner_win, 22, 70, y, x)
        twin.bkgd(" ", curses.color_pair(3))
        inner_win_beg = inner_win.getbegyx()
        twin_pos = twin.getparyx()
        twin_beg = twin.getbegyx()
        twin_max = twin.getmaxyx()
        twin.addstr(3, 0, "twin getparyx r: {} c: {}".format(twin_pos[0], twin_pos[1]))
        twin.addstr(4, 0, "twin getbegyx r: {} c: {}".format(twin_beg[0], twin_beg[1]))
        twin.addstr(5, 0, "twin getmaxyx r: {} c: {}".format(twin_max[0], twin_max[1]))
        twin.addstr(6, 0, "twin = subwin_relative(mwin, 22, 70, {}, {})".format(y, x))
        inner_win.addstr(twin_beg[0], twin_beg[1], "X - getbegyx() relative to inner_win - WRONG")
        stdscr.addstr(twin_beg[0], twin_beg[1], "Y - getbegyx() relative to stdscr - CORRECT")
        # getparyx() returns the offset within the parent of the windows top left corner
        # to get the absolute corordinates of the win's top left corner
        # muts add parrent.getbegyx() result
        stdscr.addstr(inner_win_beg[0] + twin_pos[0], inner_win_beg[1] + twin_pos[1], "Z - getparyx() relative to stdscr - if subwin top left")

        for i in range(0, twin_max[0]):
            twin.addstr(i, 45, "Y{}".format(i))
        for i in range(0, twin_max[1]):
            twin.addstr(17, i, "{}".format(i // 10))
            twin.addstr(18, i, "{}".format(i % 10))
        return twin


    inner_win = innerf(1, 1)
    twin1 = twinf(stdscr, inner_win, 9, 8)
    twin2 = twinf2(stdscr, inner_win, 9, 100)

    swin1 = subwin_relative(inner_win, 20, 40, 35, 25)
    swin1.bkgd(" ", curses.color_pair(4))

    swin2 = subwin_relative(swin1, 19, 39, 1, 1)
    swin2.bkgd(" ", curses.color_pair(5))
 
    try:

        swin3 = subwin_relative(swin1, 20, 40, 1, 0)
        swin3.bkgd(" ", curses.color_pair(3))

    except Exception:
        stdscr.addstr(59, 0, "swin3 failed as expected")
        pass # expected this one to fail

    stdscr.noutrefresh()
    mwin.noutrefresh()
    twin1.noutrefresh()
    twin2.noutrefresh()
    curses.doupdate()


    ch = " "
    while ch != "q":
        ch = stdscr.getkey()

curses.wrapper(main)


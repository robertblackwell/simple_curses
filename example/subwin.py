import curses

from numpy import inner


def subwin_relative(win, row_count, col_count, relative_begin_y, relative_begin_x):
    parent_top_left = win.getbegyx()
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
    # mwin_pos = mwin.getparyx()
    # mwin_begin = mwin.getbegyx()
    # mwin.addstr(50, 0, "getparyx r: {} c: {}".format(mwin_pos[0], mwin_pos[1]))
    # mwin.addstr(51, 0, "getbeginyx r: {} c: {}".format(mwin_begin[0], mwin_begin[1]))

    # inner_win = mwin.subwin(h, w, 1, 1)
    inner_win = subwin_relative(mwin, h, w, 1, 1)
    inner_win.bkgd(" ", curses.color_pair(1))
    # inner_win_pos = inner_win.getparyx()
    # inner_win_beg = inner_win.getbegyx()
    # inner_win.addstr(1, 0, "inner_win getparyx r: {} c: {}".format(inner_win_pos[0], inner_win_pos[1]))
    # inner_win.addstr(2, 0, "inner_win getbegyx r: {} c: {}".format(inner_win_beg[0], inner_win_beg[1]))

    twin = subwin_relative(inner_win, 10, 50, 6, 6)
    twin.bkgd(" ", curses.color_pair(3))
    # twin_pos = twin.getparyx()
    # twin_beg = twin.getbegyx()
    # twin.addstr(1, 0, "twin getparyx r: {} c: {}".format(twin_pos[0], twin_pos[1]))
    # twin.addstr(2, 0, "twin getbegyx r: {} c: {}".format(twin_beg[0], twin_beg[1]))
    # twin.addstr(3, 0, "twin = subwin_relative(mwin, 10, 50, 6, 6)")

    msg_height = 5
    menu_height = 5
    body_height = h - msg_height - menu_height

    title = "This Is A Title"
    # tcol = (120 + 2 - len(title)) // 2
    # mwin.addstr(0, tcol, title, curses.color_pair(6) + curses.A_BOLD)

    addstr_middle(mwin, 0, title, curses.color_pair(6) + curses.A_BOLD)

    win_body = subwin_relative(inner_win, body_height, w, 0, 0)
    win_body.bkgd(" ", curses.color_pair(2))

    win_menu = subwin_relative(inner_win, menu_height-1, w, body_height + 1, 0)
    win_menu.bkgd(" ", curses.color_pair(2))

    win_msg = subwin_relative(inner_win, msg_height-1, w, body_height + menu_height + 1, 0)
    win_msg.bkgd(" ", curses.color_pair(2))

    win_body_left = subwin_relative(win_body, body_height, (w // 2) - 1, 0, 0)
    win_body_left.bkgd(" ", curses.color_pair(3))

    win_body_right = subwin_relative(win_body, body_height, (w // 2), 0, (w // 2))
    win_body_right.bkgd(" ", curses.color_pair(4))


    stdscr.noutrefresh()
    mwin.noutrefresh()
    twin.noutrefresh()
    win_body.noutrefresh()
    win_body_left.noutrefresh()
    win_body_right.noutrefresh()
    curses.doupdate()


    ch = " "
    while ch != "q":
        ch = stdscr.getkey()

curses.wrapper(main)


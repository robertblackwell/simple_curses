import curses
from linecache import lazycache

from layout import VerticalStack, HorizontalStack, WidgetPosition
from dummy_widget import DummyWidget, DummyShortWidget

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

data = "context data"
left_widgets = [ 
    DummyWidget("ipnet_01",     "One     ", 30, 1, "", data),
    DummyWidget("int_val_01",   "Two     ", 30, 3, "", data),
    DummyWidget("float_val_01", "Three   ", 30, 4, "", data),
    DummyWidget("ipaddr_01",    "Four    ", 30, 2, "", data),
    DummyWidget("text_01",      "Five    ", 30, 1, "", data),
]
right_widgets = [
    DummyShortWidget("ipnet_01",     "  One  ", 8, 5, "", data),
    DummyShortWidget("int_val_01",   "  Two  ", 8, 5, "", data),
    DummyShortWidget("float_val_01", " Three ", 8, 5, "", data),
    DummyShortWidget("ipaddr_01",    "  Four ", 8, 5, "", data),
    DummyShortWidget("text_01",      "  Five ", 8, 5, "", data),
]

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

    layoutleft = VerticalStack(win_body_left.getbegyx(), win_body_left.getmaxyx(), left_widgets)
    widget_positions = layoutleft.compute_layout()

    toggle = True
    wp: WidgetPosition
    for wp in widget_positions:
        w: DummyWidget = wp.widget
        w.set_enclosing_window(subwin_relative(win_body_left, w.get_height(), w.get_width(), wp.beg_y, wp.beg_x ))
        w.color_pair = curses.color_pair(2) if toggle else curses.color_pair(6)
        toggle = not toggle

    x1 = win_menu.getparyx()
    x2 = win_menu.getbegyx()
    x3 = win_menu.getmaxyx()

    layoutright = HorizontalStack(win_menu.getmaxyx(), right_widgets)
    right_widget_positions = layoutright.compute_layout()

    wp2: WidgetPosition
    for wp2 in right_widget_positions:
        w: DummyWidget = wp2.widget
        wtmp = subwin_relative(win_menu, w.get_height() - 1, w.get_width(), wp2.beg_y, wp2.beg_x )
        w.set_enclosing_window(wtmp)
        w.color_pair = curses.color_pair(3) if toggle else curses.color_pair(4)
        toggle = not toggle



    stdscr.noutrefresh()
    mwin.noutrefresh()
    twin.noutrefresh()
    win_body.noutrefresh()
    win_body_left.noutrefresh()
    win_body_right.noutrefresh()
    for w in left_widgets:
        w.render()
    for w in right_widgets:
        w.render()
    curses.doupdate()


    ch = " "
    while ch != "q":
        ch = stdscr.getkey()

curses.wrapper(main)


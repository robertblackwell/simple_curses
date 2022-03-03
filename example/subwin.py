import curses

def main(stdscr):
    curses.curs_set(2)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_YELLOW)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_CYAN)


    stdscr.bkgd(" ", curses.color_pair(2))
    # mwin = curses.newwin(60, 120, 2, 2)
    mwin = stdscr.subwin(60, 120, 2, 2)
    mwin_pos = mwin.getparyx()
    mwin_begin = mwin.getbegyx()
    mwin.bkgd(" ", curses.color_pair(1))
    mwin.addstr(50, 0, "getparyx r: {} c: {}".format(mwin_pos[0], mwin_pos[1]))
    mwin.addstr(51, 0, "getbeginyx r: {} c: {}".format(mwin_begin[0], mwin_begin[1]))

    swin = mwin.subwin(20,50, 2, 2)
    swin.bkgd(" ", curses.color_pair(3))
    swin_pos = swin.getparyx()
    swin_beg = swin.getbegyx()
    swin.addstr(1, 0, "swin getparyx r: {} c: {}".format(swin_pos[0], swin_pos[1]))
    swin.addstr(2, 0, "swin getbegyx r: {} c: {}".format(swin_beg[0], swin_beg[1]))
    stdscr.noutrefresh()
    mwin.noutrefresh()
    curses.doupdate()


    ch = " "
    while ch != "q":
        ch = stdscr.getkey()

curses.wrapper(main)


import curses
from linecache import lazycache


def newwin_after(prev_win, h, w, xstart):
    ybeg, xbeg = prev_win.getbegyx()
    ymax, xmax = prev_win.getmaxyx()
    win = curses.newwin(h, w, ybeg + ymax, xstart)
    return win
def hline_after(prev_win):
    ybeg, xbeg = prev_win.getbegyx()
    ymax, xmax = prev_win.getmaxyx()
    win = curses.newwin(1, xmax+2, ybeg + ymax, 0)
    return win
def newwin_inside(hostwin, h, w, y, x):
    ybeg, xbeg = hostwin.getbegyx()
    ymax, xmax = hostwin.getmaxyx()
    win = curses.newwin(h, w, ybeg + y, xbeg + x)
    return win

def draw_hline(win):
    win.border(0, 0, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_LTEE, curses.ACS_RTEE, curses.ACS_LTEE, curses.ACS_RTEE)

class Frame:
    def __init__(self, stdscr, topmenu_height, body_height, msg_height, body_width):
        self.stdscr = stdscr
        self.topmenu_height = topmenu_height
        self.body_height = body_height
        self.msg_height = msg_height
        self.height = 1 + topmenu_height + 1 + body_height + 1 + msg_height + 1
        self.body_width = body_width
        self.width = 1 + body_width + 1
        
        self.outter      = curses.newwin(self.height,      self.width,       0,          0)
        self.topmenu     = newwin_inside(self.outter,      self.topmenu_height, self.body_width, 1, 1)
        self.tophline    = hline_after  (self.topmenu)
        self.bodywin     = newwin_after (self.tophline,    self.body_height,    self.body_width, 1)
        self.bottomhline = hline_after  (self.bodywin)
        self.msgwin      = newwin_after (self.bottomhline, self.msg_height,     self.body_width, 1)
    
    def render(self):
        self.outter.box()
        self.topmenu.bkgd(" ", curses.color_pair(2))
        self.topmenu.addstr(0, 0, "This is top menu", curses.A_BOLD)
        draw_hline(self.tophline)

        self.bodywin.bkgd(" ", curses.color_pair(2))
        self.bodywin.addstr(0, 0, "This is body win", curses.A_BOLD)
        draw_hline(self.bottomhline)
        self.msgwin.bkgd(" ", curses.color_pair(2))
        self.msgwin.addstr(0, 0, "This is msgwin", curses.A_BOLD)
        
        self.stdscr.noutrefresh()
        self.outter.noutrefresh()
        self.topmenu.noutrefresh()
        self.tophline.noutrefresh()
        self.bodywin.noutrefresh()
        self.bottomhline.noutrefresh()
        self.msgwin.noutrefresh()
        curses.doupdate()


def main(stdscr):
    curses.curs_set(2)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_WHITE)

    mx = stdscr.getmaxyx()

    msg_height = 5
    menu_height = 5
    body_height = 5
    body_width = 50

    height = 1 + menu_height + 1 + body_height + 1 + msg_height + 1
    width = 1 + body_width + 1
    if False:
        outter      = curses.newwin(height,      width,       0,          0)
        topmenu     = newwin_inside(outter,      menu_height, body_width, 1, 1)
        tophline    = hline_after (topmenu)
        bodywin     = newwin_after (tophline,    body_height, body_width, 1)
        bottomhline = hline_after (bodywin)
        msgwin      = newwin_after (bottomhline, msg_height,  body_width, 1)

        # outter.bkgd(" ", curses.color_pair(3))
        outter.box()
        topmenu.bkgd(" ", curses.color_pair(2))
        topmenu.addstr(0, 0, "This is top menu", curses.A_BOLD)
        draw_hline(tophline)

        bodywin.bkgd(" ", curses.color_pair(2))
        bodywin.addstr(0, 0, "This is body win", curses.A_BOLD)
        draw_hline(bottomhline)
        msgwin.bkgd(" ", curses.color_pair(2))
        msgwin.addstr(0, 0, "This is msgwin", curses.A_BOLD)


        stdscr.noutrefresh()
        outter.noutrefresh()
        topmenu.noutrefresh()
        tophline.noutrefresh()
        bodywin.noutrefresh()
        bottomhline.noutrefresh()
        msgwin.noutrefresh()
        curses.doupdate()

    frame = Frame(stdscr, 5, 5, 5, 50)
    frame.render()

    ch = " "
    while ch != "q":
        ch = stdscr.getkey()

curses.wrapper(main)


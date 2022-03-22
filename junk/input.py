import curses
from linecache import lazycache

from layout import VerticalStack, HorizontalStack, WidgetPosition
from dummy_windget import DummyWidget, DummyShortWidget

N = 40
def main(stdscr):
    curses.cbreak()
    row = 0
    stdscr.timeout(500)
    ch = " "
    retry_count = 0
    while ch != "q":
        try:
            ch = stdscr.getch()
            if ch > 0:
                stdscr.addstr(row, 1, "got ch {} row: {}".format(chr(ch), row))
                row = (row + 1) % N
            else:
                stdscr.addstr(row, 1, "getch failed row: {}".format(row))
                row = (row + 1) % N
        except Exception:
            retry_count += 1
            stdscr.addstr(row, 1, "Exception")
            row = (row + 1) % N


curses.wrapper(main)


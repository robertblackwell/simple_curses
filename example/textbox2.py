import curses
from curses.textpad import Textbox, rectangle
def main(stdscr):
    curses.initscr()
    win = curses.newwin(3, 18, 2, 2)
    box = Textbox(win)
    rectangle(stdscr, 2, 2, 5, 18)
    stdscr.refresh()
    box.edit()
    stdscr.getch()
    stdscr.addstr(20, 20, "This was in the box:["+box.gather()+"]")
    stdscr.getch()

curses.wrapper(main)
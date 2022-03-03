import curses
from simple_curses.lines_buffer import LinesBuffer

class MessageBox:
    def __init__(self):
        self.lines_buffer = LinesBuffer()
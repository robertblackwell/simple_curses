import curses
from simple_curses.lines_buffer import LinesBuffer
from widget_base import WidgetBase
class MessageBox(WidgetBase):
    def __init__(self):
        self.lines_buffer = LinesBuffer()
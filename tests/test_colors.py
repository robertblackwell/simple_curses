import sys
import unittest
import curses

import string_buffer
from colors import Colors


class TestStringBufferRight(unittest.TestCase):

    def test_colors_01(self):
        print("testing colors")
        x = Colors.button_focus()
        sb = string_buffer.StringBuffer("abc", 5)
        self.assertEqual(sb.content, "abc")
        self.assertEqual(sb.display_string, "abc" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 3)

        sb.handle_left()
        sb.handle_left()


stdscr = None
if __name__ == '__main__':
    global stdscr
    stdscr = curses.initscr()
    curses.wrapper(unittest.main())

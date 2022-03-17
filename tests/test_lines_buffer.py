import sys
import unittest
import curses

import lines_buffer

lines = [
    "1 11lkjhasdfhlakjsfhlajhflakdhjfldask",
    "2 21lkjhasdfhlakjsfhlajhflakdhjfldask",
    "3 31lkjhasdfhlakjsfhlajhflakdhjfldask",
    "4 41lkjhasdfhlakjsfhlajhflakdhjfldask",
    "5 51lkjhasdfhlakjsfhlajhflakdhjfldask",
    "6 61lkjhasdfhlakjsfhlajhflakdhjfldask",
    "7 71lkjhasdfhlakjsfhlajhflakdhjfldask",
    "8 81lkjhasdfhlakjsfhlajhflakdhjfldask",
    "9 91lkjhasdfhlakjsfhlajhflakdhjfldask",
    "0 0111lkjhasdfhlakjsfhlajhflakdhjfldask",
    "A A111lkjhasdfhlakjsfhlajhflakdhjfldask",
    "B B111lkjhasdfhlakjsfhlajhflakdhjfldask",
    "C C111lkjhasdfhlakjsfhlajhflakdhjfldask",
    "D D111lkjhasdfhlakjsfhlajhflakdhjfldask",
    "E E111lkjhasdfhlakjsfhlajhflakdhjfldask",
    "F F111lkjhasdfhlakjsfhlajhflakdhjfldask",
    "10 111lkjhasdfhlakjsfhlajhflakdhjfldask",
    "11 1lkjhasdfhlakjsfhlajhflakdhjfldask",
]


class TestLinesBuffer(unittest.TestCase):

    def test_lines_buffer_01(self):
        lb: lines_buffer.LinesBuffer = lines_buffer.LinesBuffer(lines, 100, 5)
        self.assertEqual(len(lines), 18)
        self.assertEqual(lb.first_line, 13)
        self.assertEqual(lb.last_line, 18)
        # lb.print_view()
        lb.handle_up()
        lb.handle_up()
        self.assertEqual(lb.first_line, 13)
        self.assertEqual(lb.last_line, 18)
        lb.handle_up()
        lb.handle_up()
        lb.handle_up()
        self.assertEqual(lb.first_line, 12)
        self.assertEqual(lb.last_line, 17)
        lb.handle_up()
        self.assertEqual(lb.first_line, 11)
        self.assertEqual(lb.last_line, 16)
        lb.handle_up()
        self.assertEqual(lb.first_line, 10)
        self.assertEqual(lb.last_line, 15)
        lb.handle_up()
        self.assertEqual(lb.first_line, 9)
        self.assertEqual(lb.last_line, 14)
        lb.handle_up()
        self.assertEqual(lb.first_line, 8)
        self.assertEqual(lb.last_line, 13)
        lb.handle_up()
        lb.handle_up()
        lb.handle_up()
        lb.handle_up()
        lb.handle_up()
        lb.handle_up()
        lb.handle_up()
        lb.handle_up()
        self.assertEqual(lb.first_line, 0)
        self.assertEqual(lb.last_line, 5)


if __name__ == '__main__':
    unittest.main()

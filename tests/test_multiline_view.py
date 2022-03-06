import sys
import unittest
import curses
import string

from multi_line_buffer import MultiLineView2

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
lines2 = [ 
    "0 123456789A123456789B123456789C123456789D",
    "1 123456789A123456789B123456789C123456789D",
    "2 123456789A123456789B123456789C123456789D",
    "3 123456789A123456789B123456789C123456789D",
    "4 123456789A123456789B123456789C123456789D",
    "5 123456789A123456789B123456789C123456789D",
    "6 123456789A123456789B123456789C123456789D",
    "7 123456789A123456789B123456789C123",
#    012345678901234567890123456789012345678901234567890
#    000000000011111111112222222222333333333344444444445
]



class TestMultiLineView(unittest.TestCase):
    def test_multiline_view_after_end(self):
        mlv: MultiLineView2 =MultiLineView2(lines2, 2, 7, 29, 42, 5, 6)
        self.assertEqual(mlv.cursor_line_debug, "89C123X")
        self.assertEqual(mlv.lines[mlv.curs_y_buf], "89C123 ")
        self.assertEqual(mlv.lines, [ 
            "89C123456789D",
            "89C123456789D",
            "89C123456789D",
            "89C123456789D",
            "89C123456789D",
            "89C123 ",
        ])
        print("hello")
    def test_multiline_view_at_end(self):
        mlv: MultiLineView2 =MultiLineView2(lines2, 4, 7, 0, 13, 4, 0)
        self.assertEqual(mlv.cursor_line_debug, "X")
        self.assertEqual(mlv.lines[mlv.curs_y - mlv.y_begin], " ")
        self.assertEqual(mlv.lines, [ 
            "4 123456789A12",
            "5 123456789A12",
            "6 123456789A12",
            "7 123456789A12",
            " "
        ])
        print("hello")


if __name__ == '__main__':
    unittest.main()
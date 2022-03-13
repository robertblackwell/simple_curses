import sys
import unittest
import curses
import string

import multi_line_buffer
from multi_line_view import MultiLineView2

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
    "1 123456789A123456789B123456789C123456789D",
    "2 123456789A123456789B123456789C123456789D",
    "3 123456789A123456789B123456789C123456789D",
    "4 123456789A123456789B123456789C123456789D",
    "5 123456789A123456789B123456789C123456789D",
    "6 123456789A123456789B123456789C123456789D",
    "7 123456789A123456789B123456789C123456789D",
    "8 123456789A123456789B123456789C123",
]


def test_view(lines, lb: multi_line_buffer.MultiLineBuffer):
    def comp(a, b):
        if len(a) == len(b):
            for i in range(0, len(a) - 1):
                x = a[i]
                y = b[i]
                if not (a[i] == b[i]):
                    return False
            return True
        return False
    mlv: MultiLineView2 = lb.get_view()
    v1 = mlv.view_buffer
    v2 = lines[mlv.view_content_y_begin: mlv.view_content_y_end + 1]
    return comp(v1, v2)
def handle_string(ml: multi_line_buffer.MultiLineBuffer, s: str):
    for ch in s:
        if ch == '\n':
            ml.handle_newline()
        elif ch in string.printable:
            ml.handle_character(ch)
        else:
            raise RuntimeError("invalid character in string for handle string")


class TestMultiLinesBufferDelete(unittest.TestCase):

    def test_multi_line_delete_line(self):
        ar = lines[0:7].copy()
        lb: multi_line_buffer.MultiLineBuffer = multi_line_buffer.MultiLineBuffer(ar, 5, 40)
        self.assertEqual(len(lb.content), 7)
        self.assertEqual(lb.cpos_y_content, 6)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        # self.assertTrue(test_view(lines[0:7], lb))
        v1 = lb.get_view()
        lb.handle_delete_line()
        v2 = lb.get_view()
        self.assertEqual(len(lb.content), 6)
        self.assertEqual(lb.cpos_y_content, 5)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        # self.assertTrue(test_view(lines[0:6], lb))

        lb.handle_up()


if __name__ == '__main__':
   unittest.main()
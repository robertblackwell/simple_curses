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


class TestMultiLinesBufferNewline02(unittest.TestCase):

    def test_multi_line_buffer_newline(self):
        ar = lines[0:7].copy()
        lb: multi_line_buffer.MultiLineBuffer = multi_line_buffer.MultiLineBuffer(ar, 5, 40)
        self.assertEqual(len(lb.content), 7)
        self.assertEqual(lb.cpos_y_content, 6)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines[0:7], lb))
        v1 = lb.get_view()
        lb.handle_newline()
        v2 = lb.get_view()
        self.assertEqual(len(lb.content), 8)
        self.assertEqual(lb.cpos_y_content, 7)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        # e1 = lines[0:7].copy()
        # e1.insert(6, "")
        # self.assertTrue(test_view(e1, lb))

    def test_multi_line_buffer_newline_at_end(self):
        lb: multi_line_buffer.MultiLineBuffer = multi_line_buffer.MultiLineBuffer(lines2, 5, 55)
        self.assertEqual(len(lb.content), 8)
        self.assertEqual(lb.cpos_y_content, 7)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        v1 = lb.get_view()
        lb.handle_up()
        lb.handle_up()
        for i in range(0, 43):
            lb.handle_right()
        v2 = lb.get_view()
        self.assertEqual(len(lb.content), 8)
        self.assertEqual(lb.cpos_y_content, 5)
        self.assertEqual(lb.cpos_y_buffer, 2)
        self.assertEqual(lb.cpos_x_buffer, 42)
        self.assertEqual(lb.cpos_x_content, 42)
        lb.handle_newline()
        v3 = lb.get_view()
        self.assertEqual(len(lb.content), 9)
        self.assertEqual(lb.cpos_y_content, 6)
        self.assertEqual(lb.cpos_y_buffer, 3)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertEqual(lb.content[lb.cpos_y_content], "")

    def test_multi_line_buffer_newline_at_start(self):
        ar = lines[0:7].copy()
        lb: multi_line_buffer.MultiLineBuffer = multi_line_buffer.MultiLineBuffer(ar, 5, 40)
        self.assertEqual(len(lb.content), 7)
        self.assertEqual(lb.cpos_y_content, 6)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        # self.assertTrue(test_view(lines[0:7], lb))
        v1 = lb.get_view()
        for i in range(0, 10):
            lb.handle_up()
        for i in range(0,20):
            lb.handle_left()
        v2 = lb.get_view()
        self.assertEqual(len(lb.content), 7)
        self.assertEqual(lb.cpos_y_content, 0)
        self.assertEqual(lb.cpos_y_buffer, 0)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)

        lb.handle_newline()
        self.assertEqual(len(lb.content), 8)
        self.assertEqual(lb.cpos_y_content, 1)
        self.assertEqual(lb.cpos_y_buffer, 1)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        # e1 = lines[0:7].copy()
        # e1.insert(6, "")
        # self.assertTrue(test_view(e1, lb))

    def test_multi_line_buffer_linefeed(self):
        lb: multi_line_buffer.MultiLineBuffer = multi_line_buffer.MultiLineBuffer(lines2, 5, 55)
        self.assertEqual(len(lb.content), 8)
        self.assertEqual(lb.cpos_y_content, 7)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        v1 = lb.get_view()
        lb.handle_up()
        lb.handle_up()
        for i in range(0, 30):
            lb.handle_right()
        v2 = lb.get_view()
        self.assertEqual(len(lb.content), 8)
        self.assertEqual(lb.cpos_y_content, 5)
        self.assertEqual(lb.cpos_y_buffer, 2)
        self.assertEqual(lb.cpos_x_buffer, 30)
        self.assertEqual(lb.cpos_x_content, 30)
        v3 = lb.get_view()
        lb.handle_newline()
        v4 = lb.get_view()
        self.assertEqual(len(lb.content), 9)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)


    def test_multi_line_buffer_linefeed_eol(self):
        lb: multi_line_buffer.MultiLineBuffer = multi_line_buffer.MultiLineBuffer(lines2, 5, 55)
        self.assertEqual(len(lb.content), 8)
        self.assertEqual(lb.cpos_y_content, 7)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        v1 = lb.get_view()
        for i in range(0, 35):
            lb.handle_right()
        v2 = lb.get_view()
        self.assertEqual(len(lb.content), 8)
        self.assertEqual(lb.cpos_y_content, 7)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.cpos_x_buffer, 35)
        self.assertEqual(lb.cpos_x_content, 35)
        v3 = lb.get_view()
        handle_string(lb, "\nzxcvbnm")
        v4 = lb.get_view()
        self.assertEqual(len(lb.content), 9)
        self.assertEqual(lb.cpos_x_buffer, 7)
        self.assertEqual(lb.cpos_x_content, 7)


if __name__ == '__main__':
   unittest.main()
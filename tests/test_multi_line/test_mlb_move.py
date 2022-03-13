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


class TestMultiLinesBufferMove01(unittest.TestCase):

    def test_multi_lines_buffer_up_down01(self):
        lb: multi_line_buffer.MultiLineBuffer = multi_line_buffer.MultiLineBuffer(lines, 5, 40)
        self.assertEqual(len(lb.content), 18)
        self.assertEqual(lb.cpos_y_content, 17)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))
        v1 = lb.get_view()
        lb.handle_up()
        v2 = lb.get_view()
        self.assertEqual(lb.cpos_y_content, 16)
        self.assertEqual(lb.cpos_y_buffer, 3)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))
        lb.handle_up()
        lb.handle_up()
        lb.handle_up()
        v3 = lb.get_view()
        self.assertEqual(lb.cpos_y_content, 13)
        self.assertEqual(lb.cpos_y_buffer, 0)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))
        lb.handle_up()
        v4 = lb.get_view()
        self.assertEqual(lb.cpos_y_content, 12)
        self.assertEqual(lb.cpos_y_buffer, 0)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))
        lb.handle_up()
        v5 = lb.get_view()
        self.assertEqual(lb.cpos_y_content, 11)
        self.assertEqual(lb.cpos_y_buffer, 0)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))
        lb.handle_up()
        lb.handle_up()
        v6 = lb.get_view()
        self.assertEqual(lb.cpos_y_content, 9)
        self.assertEqual(lb.cpos_y_buffer, 0)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))
        lb.handle_down()
        v7 = lb.get_view()
        self.assertEqual(lb.cpos_y_content, 10)
        self.assertEqual(lb.cpos_y_buffer, 1)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))
        lb.handle_down()
        lb.handle_down()
        v8 = lb.get_view()
        self.assertEqual(lb.cpos_y_content, 12)
        self.assertEqual(lb.cpos_y_buffer, 3)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))
        lb.handle_down()
        lb.handle_down()
        lb.handle_down()
        lb.handle_down()
        v9 = lb.get_view()
        self.assertEqual(lb.cpos_y_content, 16)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))
        lb.handle_down()
        v10 = lb.get_view()
        self.assertEqual(lb.cpos_y_content, 17)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))
        lb.handle_down()
        v11 = lb.get_view()
        self.assertEqual(lb.cpos_y_content, 17)
        self.assertEqual(lb.cpos_y_buffer, 4)
        # self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))

    def test_multi_line_buffer_move_complex(self):
        lb: multi_line_buffer.MultiLineBuffer = multi_line_buffer.MultiLineBuffer(lines2, 5, 55)
        self.assertEqual(len(lb.content), 8)
        self.assertEqual(lb.cpos_y_content, 7)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        v1 = lb.get_view()
        lb.handle_up()
        for i in range(0, 41):
            lb.handle_right()
        v = lb.get_view()
        self.assertEqual(len(lb.content), 8)
        self.assertEqual(lb.cpos_y_content, 6)
        self.assertEqual(lb.cpos_y_buffer, 3)
        self.assertEqual(lb.cpos_x_buffer, 41)
        self.assertEqual(lb.cpos_x_content, 41)
        v2 = lb.get_view()
        lb.handle_down()
        v3 = lb.get_view()
        self.assertEqual(len(lb.content), 8)



if __name__ == '__main__':
   unittest.main()
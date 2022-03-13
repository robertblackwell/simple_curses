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


class TestMultiLinesHelpers(unittest.TestCase):
    def test_multi_line_buffer_helpers(self):
        lb: multi_line_buffer.MultiLineBuffer = multi_line_buffer.MultiLineBuffer(lines2, 5, 55)
        self.assertEqual(len(lb.content), 8)
        self.assertEqual(lb.cpos_y_content, 7)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        lb._cursor_set_after_end()
        v = lb.get_view()
        self.assertEqual(len(lb.content), 9)
        self.assertEqual(lb.cpos_y_content, 8)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)



class TestMultiLinesBufferUtils(unittest.TestCase):

    def test_split_str(self):
        str = "123456789"
        p, s = multi_line_buffer._string_split_at_pos(str, 3)
        self.assertEqual(p, "123")
        self.assertEqual(s, "456789")
        p, s = multi_line_buffer._string_split_at_pos(str, 0)
        self.assertEqual(p, "")
        self.assertEqual(s, "123456789")
        p, s = multi_line_buffer._string_split_at_pos(str, 12)
        self.assertEqual(p, "123456789")
        self.assertEqual(s, "")

    def test_split_list_of_strings_middle(self):
        ar = lines.copy()[0: 4]
        lenbefore = len(ar)
        x = multi_line_buffer._list_split_at_line_pos(ar, 2, 6)
        self.assertEqual(len(x), lenbefore + 1)
        expected = [
            lines[0], 
            lines[1], 
            lines[2][0:6], 
            lines[2][6: len(lines[3])],
            lines[3], 
        ]
        self.assertEqual(x, expected)
        self.assertEqual(ar, expected)

    def test_split_list_of_strings_begin(self):
        ar = lines.copy()[0: 4]
        lenbefore = len(ar)
        x = multi_line_buffer._list_split_at_line_pos(ar, 0, 6)
        self.assertEqual(len(x), lenbefore + 1)
        expected = [
            lines[0][0:6],
            lines[0][6: len(lines[0])], 
            lines[1], 
            lines[2], 
            lines[3]
        ]
        self.assertEqual(x, expected)
        self.assertEqual(ar, expected)

    def test_split_list_of_strings_end(self):
        ar = lines.copy()[0: 4]
        lenbefore = len(ar)
        k = len(ar) - 1
        x = multi_line_buffer._list_split_at_line_pos(ar, k, 6)
        self.assertEqual(len(x), lenbefore + 1)
        expected = [
            lines[0], 
            lines[1], 
            lines[2], 
            lines[3][0:6], 
            lines[3][6: len(lines[3])]
        ]
        self.assertEqual(x, expected)
        self.assertEqual(ar, expected)

if __name__ == '__main__':
   unittest.main()
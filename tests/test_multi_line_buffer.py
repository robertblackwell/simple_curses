import sys
import unittest
import curses
import string

from matplotlib.pyplot import text

import multi_line_buffer

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


def test_view(lines, lb):
    def comp(a, b):
        if len(a) == len(b):
            for i in range(0, len(a) - 1):
                x = a[i]
                y = b[i]
                if not (a[i] == b[i]):
                    return False
            return True
        return False
    v1 = lb.get_view().lines
    v2 = lines[lb.view_y_begin: lb.view_y_end + 1]
    return comp(v1, v2)
def handle_string(ml: multi_line_buffer.MultiLineBuffer, s: str):
    for ch in s:
        if ch == '\n':
            ml.handle_newline()
        elif ch in string.printable:
            ml.handle_character(ch)
        else:
            raise RuntimeError("invalid character in string for handle string")
class TestMultiLinesBufferLineFeed(unittest.TestCase):
    def test_multi_line_buffer_linefeed_eol(self):
        lb: multi_line_buffer.MultiLineBuffer = multi_line_buffer.MultiLineBuffer(lines2, 5, 55)
        self.assertEqual(len(lb.content), 8)
        self.assertEqual(lb.cpos_y_content, 7)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.view_y_begin, 3)
        self.assertEqual(lb.view_y_end, 7)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        for i in range(0, 35):
            lb.handle_right()
        v = lb.get_view()
        self.assertEqual(len(lb.content), 8)
        self.assertEqual(lb.cpos_y_content, 7)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.view_y_begin, 3)
        self.assertEqual(lb.view_y_end, 7)
        self.assertEqual(lb.cpos_x_buffer, 35)
        self.assertEqual(lb.cpos_x_content, 35)
        v2 = lb.get_view()
        handle_string(lb, "\nzxcvbnm")
        v3 = lb.get_view()
        self.assertEqual(len(lb.content), 9)
        self.assertEqual(v3.lines[3], "8 123456789A123456789B123456789C123")
        self.assertEqual(v3.lines[3], "zxcvbnm")
        self.assertEqual(lb.cpos_x_buffer, 7)
        self.assertEqual(lb.cpos_x_content, 7)

    def test_multi_line_buffer_linefeed(self):
        lb: multi_line_buffer.MultiLineBuffer = multi_line_buffer.MultiLineBuffer(lines2, 5, 55)
        self.assertEqual(len(lb.content), 8)
        self.assertEqual(lb.cpos_y_content, 7)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.view_y_begin, 3)
        self.assertEqual(lb.view_y_end, 7)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        lb.handle_up()
        lb.handle_up()
        for i in range(0, 30):
            lb.handle_right()
        v = lb.get_view()
        self.assertEqual(len(lb.content), 8)
        self.assertEqual(lb.cpos_y_content, 5)
        self.assertEqual(lb.cpos_y_buffer, 2)
        self.assertEqual(lb.view_y_begin, 3)
        self.assertEqual(lb.view_y_end, 7)
        self.assertEqual(lb.cpos_x_buffer, 30)
        self.assertEqual(lb.cpos_x_content, 30)
        v2 = lb.get_view()
        lb.handle_newline()
        v3 = lb.get_view()
        self.assertEqual(len(lb.content), 9)
        self.assertEqual(v3.lines[2], "6 123456789A123456789B12345678")
        self.assertEqual(v3.lines[3], "9C123456789D")
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)

class TestMultiLinesBufferComplex(unittest.TestCase):
    def test_multi_line_buffer_complex(self):
        lb: multi_line_buffer.MultiLineBuffer = multi_line_buffer.MultiLineBuffer(lines2, 5, 55)
        self.assertEqual(len(lb.content), 8)
        self.assertEqual(lb.cpos_y_content, 7)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.view_y_begin, 3)
        self.assertEqual(lb.view_y_end, 7)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        lb.handle_up()
        for i in range(0, 41):
            lb.handle_right()
        v = lb.get_view()
        self.assertEqual(len(lb.content), 8)
        self.assertEqual(lb.cpos_y_content, 6)
        self.assertEqual(lb.cpos_y_buffer, 3)
        self.assertEqual(lb.view_y_begin, 3)
        self.assertEqual(lb.view_y_end, 7)
        self.assertEqual(lb.cpos_x_buffer, 41)
        self.assertEqual(lb.cpos_x_content, 41)
        v2 = lb.get_view()
        lb.handle_down()
        v3 = lb.get_view()
        self.assertEqual(len(lb.content), 8)


class TestMultiLinesBuffer(unittest.TestCase):

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

    def test_multi_line_newline(self):
        ar = lines[0:7].copy()
        lb: multi_line_buffer.MultiLineBuffer = multi_line_buffer.MultiLineBuffer(ar, 5, 40)
        self.assertEqual(len(lb.content), 7)
        self.assertEqual(lb.cpos_y_content, 6)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.view_y_begin, 2)
        self.assertEqual(lb.view_y_end, 6)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines[0:7], lb))

        lb.handle_newline()
        self.assertEqual(len(lb.content), 8)
        self.assertEqual(lb.cpos_y_content, 7)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.view_y_begin, 3)
        self.assertEqual(lb.view_y_end, 7)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        e1 = lines[0:7].copy()
        e1.insert(6, "")
        self.assertTrue(test_view(e1, lb))

    def test_multi_line_delete_line(self):
        ar = lines[0:7].copy()
        lb: multi_line_buffer.MultiLineBuffer = multi_line_buffer.MultiLineBuffer(ar, 5, 40)
        self.assertEqual(len(lb.content), 7)
        self.assertEqual(lb.cpos_y_content, 6)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.view_y_begin, 2)
        self.assertEqual(lb.view_y_end, 6)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines[0:7], lb))

        lb.handle_delete_line()
        self.assertEqual(len(lb.content), 6)
        self.assertEqual(lb.cpos_y_content, 5)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.view_y_begin, 2)
        self.assertEqual(lb.view_y_end, 6)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines[0:6], lb))

        lb.handle_up()

    def test_multi_line_buffer_addline(self):
        lb: multi_line_buffer.MultiLineBuffer = multi_line_buffer.MultiLineBuffer([], 5, 40)
        self.assertEqual(len(lb.content), 1)
        self.assertEqual(lb.cpos_y_content, 0)
        self.assertEqual(lb.cpos_y_buffer, 0)
        self.assertEqual(lb.view_y_begin, 0)
        self.assertEqual(lb.view_y_end, 0)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))
        lb.append_line(lines[1])
        self.assertEqual(len(lb.content), 1)
        self.assertEqual(lb.cpos_y_content, 0)
        self.assertEqual(lb.cpos_y_buffer, 0)
        self.assertEqual(lb.view_y_begin, 0)
        self.assertEqual(lb.view_y_end, 0)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))
        lb.append_line(lines[2])
        self.assertEqual(len(lb.content), 2)
        self.assertEqual(lb.cpos_y_content, 1)
        self.assertEqual(lb.cpos_y_buffer, 1)
        self.assertEqual(lb.view_y_begin, 0)
        self.assertEqual(lb.view_y_end, 1)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines[1:3], lb))

    def test_multi_line_buffer_addline_in_constructor(self):
        lb: multi_line_buffer.MultiLineBuffer = multi_line_buffer.MultiLineBuffer([lines[0], lines[1]], 5, 40)
        self.assertEqual(len(lb.content), 2)
        self.assertEqual(lb.cpos_y_content, 1)
        self.assertEqual(lb.cpos_y_buffer, 1)
        self.assertEqual(lb.view_y_begin, 0)
        self.assertEqual(lb.view_y_end, 1)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        # self.assertTrue(test_view(lines, lb))
        lb.append_line(lines[1])
        self.assertEqual(len(lb.content), 3)
        self.assertEqual(lb.cpos_y_content, 2)
        self.assertEqual(lb.cpos_y_buffer, 2)
        self.assertEqual(lb.view_y_begin, 0)
        self.assertEqual(lb.view_y_end, 2)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        # self.assertTrue(test_view(lines, lb))
        lb.append_line(lines[2])
        self.assertEqual(len(lb.content), 4)
        self.assertEqual(lb.cpos_y_content, 3)
        self.assertEqual(lb.cpos_y_buffer, 3)
        self.assertEqual(lb.view_y_begin, 0)
        self.assertEqual(lb.view_y_end, 3)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        # self.assertTrue(test_view(lines[1:3], lb))


    def test_multi_lines_buffer_up_down01(self):
        lb: multi_line_buffer.MultiLineBuffer = multi_line_buffer.MultiLineBuffer(lines, 5, 40)
        self.assertEqual(len(lb.content), 18)
        self.assertEqual(lb.cpos_y_content, 17)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.view_y_begin, 13)
        self.assertEqual(lb.view_y_end, 17)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))
        lb.handle_up()
        self.assertEqual(lb.cpos_y_content, 16)
        self.assertEqual(lb.cpos_y_buffer, 3)
        self.assertEqual(lb.view_y_begin, 13)
        self.assertEqual(lb.view_y_end, 17)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))
        lb.handle_up()
        lb.handle_up()
        lb.handle_up()
        self.assertEqual(lb.cpos_y_content, 13)
        self.assertEqual(lb.cpos_y_buffer, 0)
        self.assertEqual(lb.view_y_begin, 13)
        self.assertEqual(lb.view_y_end, 17)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))
        lb.handle_up()
        self.assertEqual(lb.cpos_y_content, 12)
        self.assertEqual(lb.cpos_y_buffer, 0)
        self.assertEqual(lb.view_y_begin, 12)
        self.assertEqual(lb.view_y_end, 16)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))
        lb.handle_up()
        self.assertEqual(lb.cpos_y_content, 11)
        self.assertEqual(lb.cpos_y_buffer, 0)
        self.assertEqual(lb.view_y_begin, 11)
        self.assertEqual(lb.view_y_end, 15)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))
        lb.handle_up()
        lb.handle_up()
        self.assertEqual(lb.cpos_y_content, 9)
        self.assertEqual(lb.cpos_y_buffer, 0)
        self.assertEqual(lb.view_y_begin, 9)
        self.assertEqual(lb.view_y_end, 13)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))
        lb.handle_down()
        self.assertEqual(lb.cpos_y_content, 10)
        self.assertEqual(lb.cpos_y_buffer, 1)
        self.assertEqual(lb.view_y_begin, 9)
        self.assertEqual(lb.view_y_end, 13)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))
        lb.handle_down()
        lb.handle_down()
        self.assertEqual(lb.cpos_y_content, 12)
        self.assertEqual(lb.cpos_y_buffer, 3)
        self.assertEqual(lb.view_y_begin, 9)
        self.assertEqual(lb.view_y_end, 13)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))
        lb.handle_down()
        lb.handle_down()
        lb.handle_down()
        lb.handle_down()
        self.assertEqual(lb.cpos_y_content, 16)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.view_y_begin, 12)
        self.assertEqual(lb.view_y_end, 16)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))
        lb.handle_down()
        self.assertEqual(lb.cpos_y_content, 17)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.view_y_begin, 13)
        self.assertEqual(lb.view_y_end, 17)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))
        lb.handle_down()
        self.assertEqual(lb.cpos_y_content, 17)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.view_y_begin, 13)
        self.assertEqual(lb.view_y_end, 17)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        self.assertTrue(test_view(lines, lb))



if __name__ == '__main__':
   unittest.main()
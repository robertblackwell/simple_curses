import sys
import unittest
import curses
import string

from simple_curses.multi_line_buffer import MultiLineBuffer
from simple_curses.multi_line_view import MultiLineView2

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


def test_view(lines, lb: MultiLineBuffer):
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
def handle_string(ml: MultiLineBuffer, s: str):
    for ch in s:
        if ch == '\n':
            ml.handle_newline()
        elif ch in string.printable:
            ml.handle_character(ch)
        else:
            raise RuntimeError("invalid character in string for handle string")

class TestGetViewOnBSJoinVeryLongLine(unittest.TestCase):
    def test_getview_on_bs_join_long_lines(self):
        ar = ["".join(lines[0:2].copy()), "".join(lines[2:4].copy())]
        lb: MultiLineBuffer = MultiLineBuffer(ar, 5, 40)
        self.assertEqual(len(lb.content), 2)
        self.assertEqual(lb.cpos_y_content, 1)
        self.assertEqual(lb.cpos_y_buffer, 1)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        v0 = lb.get_view()
        lb.handle_backspace()
        self.assertEqual(len(lb.content), 1)
        self.assertEqual(lb.cpos_y_content, 0)
        self.assertEqual(lb.cpos_y_buffer, 0)
        self.assertEqual(lb.cpos_x_buffer, 39)
        self.assertEqual(lb.cpos_x_content, 74)
        v1 = lb.get_view()
        print("")

class TestBackspaceJoinEmptyToNonEmpty(unittest.TestCase):
    def test_join_empty_to_non_empty(self):
        """
        Tests situation where content is two lines, first is empy second is not empty
        cursor is at start of secoond line
        then backspace
        """
        ar = lines[0:1].copy()
        lb: MultiLineBuffer = MultiLineBuffer(ar, 5, 40)
        # position to start of only line
        for i in range(0, len(ar[0]) + 5):
            lb.handle_left()
        v0 = lb.get_view()
        self.assertEqual(len(lb.content), 1)
        self.assertEqual(lb.cpos_y_content, 0)
        self.assertEqual(lb.cpos_y_buffer, 0)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        lb.handle_newline()
        v1 = lb.get_view()
        self.assertEqual(len(lb.content), 2)
        self.assertEqual(lb.cpos_y_content, 1)
        self.assertEqual(lb.cpos_y_buffer, 1)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        # lb.handle_up()
        # # self.assertTrue(test_view(lines[0:7], lb))
        # v2 = lb.get_view()
        # self.assertEqual(len(lb.content), 2)
        # self.assertEqual(lb.cpos_y_content, 0)
        # self.assertEqual(lb.cpos_y_buffer, 0)
        # self.assertEqual(lb.cpos_x_buffer, 0)
        # self.assertEqual(lb.cpos_x_content, 0)
        lb.handle_backspace()
        # v3 = lb.get_view()
        self.assertEqual(len(lb.content), 1)
        self.assertEqual(lb.cpos_y_content, 0)
        self.assertEqual(lb.cpos_y_buffer, 0)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)

class TestBackspaceOnEmptyLine(unittest.TestCase):
    def test_backspace_on_empty_line(self):
        ar = lines[0:7].copy()
        lb: MultiLineBuffer = MultiLineBuffer(ar, 5, 40)
        for i in range(0, 3):
            lb.handle_up()
        for i in range(0, len(ar[6]) + 5):
            lb.handle_right()
        v0 = lb.get_view()
        self.assertEqual(len(lb.content), 7)
        self.assertEqual(lb.cpos_y_content, 3)
        self.assertEqual(lb.cpos_y_buffer, 1)
        self.assertEqual(lb.cpos_x_buffer, 37)
        self.assertEqual(lb.cpos_x_content, 37)
        lb.handle_newline()
        v1 = lb.get_view()
        self.assertEqual(len(lb.content), 8)
        self.assertEqual(lb.cpos_y_content, 4)
        self.assertEqual(lb.cpos_y_buffer, 2)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        # self.assertTrue(test_view(lines[0:7], lb))
        v2 = lb.get_view()
        lb.handle_backspace()
        v3 = lb.get_view()
        self.assertEqual(len(lb.content), 7)
        self.assertEqual(lb.cpos_y_content, 3)
        self.assertEqual(lb.cpos_y_buffer, 1)
        self.assertEqual(lb.cpos_x_buffer, 37)
        self.assertEqual(lb.cpos_x_content, 37)

class TestMultiLinesBackspaceAtEndOfContent(unittest.TestCase):

    def test_backspace_at_end_of_content(self):
        ar = lines[0:7].copy()
        lb: MultiLineBuffer = MultiLineBuffer(ar, 5, 40)
        for i in range(0, 8):
            lb.handle_down()
        for i in range(0, len(ar[6]) + 5):
            lb.handle_right()
        v0 = lb.get_view()
        self.assertEqual(len(lb.content), 7)
        self.assertEqual(lb.cpos_y_content, 6)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.cpos_x_buffer, 37)
        self.assertEqual(lb.cpos_x_content, 37)
        lb.handle_newline()
        v1 = lb.get_view()
        self.assertEqual(len(lb.content), 8)
        self.assertEqual(lb.cpos_y_content, 7)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        # self.assertTrue(test_view(lines[0:7], lb))
        v2 = lb.get_view()
        lb.handle_backspace()
        v3 = lb.get_view()
        self.assertEqual(len(lb.content), 7)
        self.assertEqual(lb.cpos_y_content, 6)
        self.assertEqual(lb.cpos_y_buffer, 3)
        self.assertEqual(lb.cpos_x_buffer, 37)
        self.assertEqual(lb.cpos_x_content, 37)
        # self.assertTrue(test_view(lines[0:6], lb))

class TestMultiLineBufferBackspace(unittest.TestCase):
    def test_backspace_inside_line(self):
        ar = lines[0:7].copy()
        lb: MultiLineBuffer = MultiLineBuffer(ar, 5, 40)
        self.assertEqual(len(lb.content), 7)
        self.assertEqual(lb.cpos_y_content, 6)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        # cursor is at at start of last line
        for i in range(0,2):
            lb.handle_right()
        # cursor is no inside last line
        lb.handle_backspace()
        self.assertEqual(len(lb.content), 7)
        self.assertEqual(lb.cpos_y_content, 6)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.cpos_x_buffer, 1)
        self.assertEqual(lb.cpos_x_content, 1)

    def test_backspace_start_of_line(self):
        ar = lines[0:7].copy()
        lb: MultiLineBuffer = MultiLineBuffer(ar, 5, 40)
        self.assertEqual(len(lb.content), 7)
        self.assertEqual(lb.cpos_y_content, 6)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        # cursor is at at start of last line
        lb.handle_up()
        # cursor is now at start of second last line
        lb.handle_backspace()
        self.assertEqual(len(lb.content), 6)
        self.assertEqual(lb.cpos_y_content, 4)
        self.assertEqual(lb.cpos_y_buffer, 2)
        self.assertEqual(lb.cpos_x_buffer, 37)
        self.assertEqual(lb.cpos_x_content, 37)

    def test_backspace_end_of_line(self):
        ar = lines[0:7].copy()
        lb: MultiLineBuffer = MultiLineBuffer(ar, 5, 40)
        self.assertEqual(len(lb.content), 7)
        self.assertEqual(lb.cpos_y_content, 6)
        self.assertEqual(lb.cpos_y_buffer, 4)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        # cursor is at at start of last line
        lb.handle_up()
        self.assertEqual(len(lb.content), 7)
        self.assertEqual(lb.cpos_y_content, 5)
        self.assertEqual(lb.cpos_y_buffer, 3)
        self.assertEqual(lb.cpos_x_buffer, 0)
        self.assertEqual(lb.cpos_x_content, 0)
        v1 = lb.get_view()
        for i in range(0,40):
            lb.handle_right()
        v2 = lb.get_view()
        self.assertEqual(len(lb.content), 7)
        self.assertEqual(lb.cpos_y_content, 5)
        self.assertEqual(lb.cpos_y_buffer, 3)
        self.assertEqual(lb.cpos_x_buffer, 37)
        self.assertEqual(lb.cpos_x_content, 37)
        # cursor is no at end of second last line
        lb.handle_backspace()
        # should have combined second last and last lines
        v3 = lb.get_view()
        self.assertEqual(len(lb.content), 7)
        self.assertEqual(lb.cpos_y_content, 5)
        self.assertEqual(lb.cpos_y_buffer, 3)
        self.assertEqual(lb.cpos_x_buffer, 36)
        self.assertEqual(lb.cpos_x_content,36)

if __name__ == '__main__':
   unittest.main()
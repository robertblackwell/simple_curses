import sys
import unittest
import curses

from matplotlib.pyplot import text

import text_buffer

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
    v1 = lb.get_view()
    v2 = lines[lb.view_y_begin: lb.view_y_end + 1]
    return comp(v1, v2)

class TestMultiLinesBuffer(unittest.TestCase):

    def test_split_str(self):
        str = "123456789"
        p, s = text_buffer._string_split_at_pos(str, 3)
        self.assertEqual(p, "123")
        self.assertEqual(s, "456789")
        p, s = text_buffer._string_split_at_pos(str, 0)
        self.assertEqual(p, "")
        self.assertEqual(s, "123456789")
        p, s = text_buffer._string_split_at_pos(str, 12)
        self.assertEqual(p, "123456789")
        self.assertEqual(s, "")

    def test_split_list_of_strings_middle(self):
        ar = lines.copy()[0: 4]
        lenbefore = len(ar)
        x = text_buffer._list_split_at_line_pos(ar, 2, 6)
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
        x = text_buffer._list_split_at_line_pos(ar, 0, 6)
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
        x = text_buffer._list_split_at_line_pos(ar, k, 6)
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
        lb: text_buffer.TextBuffer = text_buffer.TextBuffer(ar, 5, 40)
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
        lb: text_buffer.TextBuffer = text_buffer.TextBuffer(ar, 5, 40)
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


    def test_multi_lines_buffer_up_down01(self):
        lb: text_buffer.TextBuffer = text_buffer.TextBuffer(lines, 5, 40)
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
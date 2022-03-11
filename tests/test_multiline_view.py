import sys
import unittest
import curses
import string

from multi_line_buffer import MultiLineView2

lines = [
    "0 0111lkjhasdfhlakjsfhlajhflakdhjfldask",
    "1 11lkjhasdfhlakjsfhlajhflakdhjfldask",
    "2 21lkjhasdfhlakjsfhlajhflakdhjfldask",
    "3 31lkjhasdfhlakjsfhlajhflakdhjfldask",
    "4 41lkjhasdfhlakjsfhlajhflakdhjfldask",
    "5 51lkjhasdfhlakjsfhlajhflakdhjfldask",
    "6 61lkjhasdfhlakjsfhlajhflakdhjfldask",
    "7 71lkjhasdfhlakjsfhlajhflakdhjfldask",
    "8 81lkjhasdfhlakjsfhlajhflakdhjfldask",
    "9 91lkjhasdfhlakjsfhlajhflakdhjfldask",
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
    "7 123456789A123456789B123456789C123456789D",
    "8 123456789A123456789B123456789C123456789D",
    "9 123456789A123456789B123456789C123456789D",
    "A 123456789A123456789B123456789C123456789D",
    "B 123456789A123456789B123456789C123",
#    012345678901234567890123456789012345678901234567890
#    000000000011111111112222222222333333333344444444445
]
lines_short = lines2[0:10]
lines_very_short = lines2[0:6]


class TestMultiLineView_Debug_Y_Cases(unittest.TestCase):

    def test_multiline_view_case1(self):
        height = 7
        self.assertEqual(len(lines), 18)
        mlv: MultiLineView2 = MultiLineView2(content_lines=lines, \
            cpos_y_content = 7,  \
            cpos_x_content = 7,  \
            view_height    = height,  \
            view_width     = 12, \
            cpos_y_buffer  = 2,  \
            cpos_x_buffer  = 7)
        b = mlv.make_debug()
        expected =  [
            lines[5], 
            lines[6], 
            lines[7], 
            lines[8], 
            lines[9],
            lines[10],
            lines[11],
        ]
        self.assertEqual(b, expected)
        self.assertEqual(mlv.view_height, 7)
        self.assertEqual(mlv.view_content_y_begin, 5)
        self.assertEqual(mlv.view_content_y_end, 11)
        self.assertEqual(mlv.view_buffer_y_begin, 0)
        self.assertEqual(mlv.view_buffer_y_end, 6)

    def test_multiline_view_case2(self):
        height = 7
        self.assertEqual(len(lines), 18)
        mlv: MultiLineView2 = MultiLineView2(content_lines=lines, \
            cpos_y_content = len(lines),  \
            cpos_x_content = 7,  \
            view_height    = height,  \
            view_width     = 12, \
            cpos_y_buffer  = 6,  \
            cpos_x_buffer  = 7)
        b = mlv.make_debug()
        expected = [
            lines[12], 
            lines[13], 
            lines[14], 
            lines[15],
            lines[16],
            lines[17],
            "W" # indicates cursor line
        ]
        self.assertEqual(b, expected)
        self.assertEqual(mlv.view_height, 7)
        self.assertEqual(mlv.view_content_y_begin, 12)
        self.assertEqual(mlv.view_content_y_end, 18)
        self.assertEqual(mlv.view_buffer_y_begin, 0)
        self.assertEqual(mlv.view_buffer_y_end, 6)

    def test_multiline_view_case3(self):
        height = 7
        self.assertEqual(len(lines_short), 10)
        mlv: MultiLineView2 = MultiLineView2(content_lines=lines_short, \
            cpos_y_content = 7,  \
            cpos_x_content = 7,  \
            view_height    = height,  \
            view_width     = 12, \
            cpos_y_buffer  = 3,  \
            cpos_x_buffer  = 7)
        b = mlv.make_debug()
        expected = [
            lines2[4], 
            lines2[5], 
            lines2[6], 
            lines2[7],
            lines2[8],
            lines2[9],
            "Z" # indicates cursor line
        ]
        self.assertEqual(b, expected)
        self.assertEqual(mlv.view_height, 7)
        self.assertEqual(mlv.view_content_y_begin, 4)
        self.assertEqual(mlv.view_content_y_end, 9)
        self.assertEqual(mlv.view_buffer_y_begin, 0)
        self.assertEqual(mlv.view_buffer_y_end, 5)

    def test_multiline_view_case4(self):
        height = 7
        self.assertEqual(len(lines_very_short), 6)
        mlv: MultiLineView2 = MultiLineView2(content_lines=lines_very_short, \
            cpos_y_content = 3,  \
            cpos_x_content = 7,  \
            view_height    = height,  \
            view_width     = 12, \
            cpos_y_buffer  = 4,  \
            cpos_x_buffer  = 7)
        b = mlv.make_debug()
        expected = [
            "Z",
            lines_very_short[0], 
            lines_very_short[1], 
            lines_very_short[2], 
            lines_very_short[3], 
            lines_very_short[4], 
            lines_very_short[5], 
        ]
        self.assertEqual(b, expected)
        self.assertEqual(mlv.view_height, 7)
        self.assertEqual(mlv.view_content_y_begin, 0)
        self.assertEqual(mlv.view_content_y_end, 5)
        self.assertEqual(mlv.view_buffer_y_begin, 1)
        self.assertEqual(mlv.view_buffer_y_end, 6)

    def test_multiline_view_case5(self):
        height = 7
        self.assertEqual(len(lines_very_short), 6)
        mlv: MultiLineView2 = MultiLineView2(content_lines=lines_very_short, \
            cpos_y_content = 6,  \
            cpos_x_content = 7,  \
            view_height    = height,  \
            view_width     = 12, \
            cpos_y_buffer  = 6,  \
            cpos_x_buffer  = 7)
        b = mlv.make_debug()
        self.assertEqual(b, [
            lines2[0], 
            lines2[1], 
            lines2[2], 
            lines2[3],
            lines2[4],
            lines2[5],
            "W" # indicates cursor line
        ])
        self.assertEqual(mlv.view_height, 7)
        self.assertEqual(mlv.view_content_y_begin, 0)
        self.assertEqual(mlv.view_content_y_end, 6)
        self.assertEqual(mlv.view_buffer_y_begin, 0)
        self.assertEqual(mlv.view_buffer_y_end, 6)

    def test_multiline_view_case6(self):
        height = 7
        self.assertEqual(len(lines_very_short), 6)
        mlv: MultiLineView2 = MultiLineView2(content_lines=lines_very_short, \
            cpos_y_content = 3,  \
            cpos_x_content = 7,  \
            view_height    = height,  \
            view_width     = 12, \
            cpos_y_buffer  = 3,  \
            cpos_x_buffer  = 7)
        b = mlv.make_debug()
        self.assertEqual(b, [
            lines2[0], 
            lines2[1], 
            lines2[2], 
            lines2[3],
            lines2[4],
            lines2[5],
            "Z" # indicates unused line
        ])
        self.assertEqual(mlv.view_height, 7)
        self.assertEqual(mlv.view_content_y_begin, 0)
        self.assertEqual(mlv.view_content_y_end, 5)
        self.assertEqual(mlv.view_buffer_y_begin, 0)
        self.assertEqual(mlv.view_buffer_y_end, 6)

if __name__ == '__main__':
    unittest.main()
import sys
import unittest
import curses
import string

from multi_line_buffer import MultiLineBuffer, MultiLineView2

linesx = [
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
lines = [ 
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
    "B 123456789A123456789B123456789C123456789D",
    "C 123456789A123456789B123456789C123456789D",
    "D 123456789A123456789B123456789C123456789D",
    "E 123456789A123456789B123456789C123456789D",
    "F 123456789A123456789B123456789C123456789D",
    "10 123456789A123456789B123456789C123456789D",
    "11 123456789A123456789B123456789C123456789D",
#    012345678901234567890123456789012345678901234567890
#    000000000011111111112222222222333333333344444444445
]
lines_short = lines[0:10]
lines_very_short = lines[0:6]


class TestMultiLineView_Debug_Y_Cases(unittest.TestCase):


    def test_multiline_view_1(self):
        height = 7
        width = 12
        self.assertEqual(len(lines), 18)
        mlb: MultiLineBuffer = MultiLineBuffer(lines=lines, height=height, width=width)
        # put the cursor somewhere in the middle
        for i in range(0,8):
            mlb.handle_up()
        for i in range(0,16):
            mlb.handle_right() 
        self.assertEqual(len(mlb.content), 18)
        self.assertEqual(mlb.cpos_y_content, 9)
        self.assertEqual(mlb.cpos_x_content, 16)
        self.assertEqual(mlb.cpos_y_buffer, 0)
        self.assertEqual(mlb.cpos_x_buffer, 11)
        mlv: MultiLineView2 = MultiLineView2(content_lines=mlb.content, \
            cpos_y_content = mlb.cpos_y_content,  \
            cpos_x_content = mlb.cpos_x_content,  \
            view_height    = height,  \
            view_width     = width, \
            cpos_y_buffer  = mlb.cpos_y_buffer,  \
            cpos_x_buffer  = mlb.cpos_x_buffer)
        b = mlv.make_debug()
        dbg_cursor = mlv.debug_cursor_line
        buf = mlv.view_buffer
        expected =  [
            lines[9], 
            lines[10], 
            lines[11], 
            lines[12],
            lines[13],
            lines[14],
            lines[15],
        ]
        expected_buffer = [ 
            "456789A12345",
            "456789A12345",
            "456789A12345",
            "456789A12345",
            "456789A12345",
            "456789A12345",
            "456789A12345",
        ]
        self.assertEqual(b, expected)
        self.assertEqual(buf, expected_buffer)
        self.assertEqual(mlv.char_under_cursor, "5")
        self.assertEqual(mlv.view_height, 7)
        self.assertEqual(mlv.view_content_y_begin, 9)
        self.assertEqual(mlv.view_content_y_end, 15)
        self.assertEqual(mlv.view_buffer_y_begin, 0)
        self.assertEqual(mlv.view_buffer_y_end, 6)

    def test_multiline_view_2(self):
        height = 7
        width = 12
        self.assertEqual(len(lines), 18)
        mlb: MultiLineBuffer = MultiLineBuffer(lines=lines, height=height, width=width)
        # put the cursor on an empty last line at position zero
        mlb._cursor_set_after_end() 
        self.assertEqual(mlb.cpos_y_content, 18)
        self.assertEqual(mlb.cpos_x_content, 0)
        self.assertEqual(mlb.cpos_y_buffer, 6)
        self.assertEqual(mlb.cpos_x_buffer, 0)
        mlv: MultiLineView2 = MultiLineView2(content_lines=mlb.content, \
            cpos_y_content = mlb.cpos_y_content,  \
            cpos_x_content = mlb.cpos_x_content,  \
            view_height    = height,  \
            view_width     = width, \
            cpos_y_buffer  = mlb.cpos_y_buffer,  \
            cpos_x_buffer  = mlb.cpos_x_buffer)
        b = mlv.make_debug()
        dbg_cursor = mlv.debug_cursor_line
        buf = mlv.view_buffer
        expected =  [
            lines[12], 
            lines[13], 
            lines[14], 
            lines[15],
            lines[16],
            lines[17],
            ""
        ]
        expected_buffer = [ 
            "C 123456789A",            
            "D 123456789A",            
            "E 123456789A",            
            "F 123456789A",            
            "10 123456789",            
            "11 123456789",
            " "            
        ]
        self.assertEqual(b, expected)
        self.assertEqual(buf, expected_buffer)
        self.assertEqual(mlv.char_under_cursor, " ")
        self.assertEqual(mlv.view_height, 7)
        self.assertEqual(mlv.view_content_y_begin, 12)
        self.assertEqual(mlv.view_content_y_end, 18)
        self.assertEqual(mlv.view_buffer_y_begin, 0)
        self.assertEqual(mlv.view_buffer_y_end, 6)

    def test_multiline_view_3(self):
        height = 7
        width = 12
        self.assertEqual(len(lines), 18)
        mlb: MultiLineBuffer = MultiLineBuffer(lines=lines, height=height, width=width)
        # put the cursor on an empty last line at position zero
        mlb._cursor_set_after_end() 
        # move the cursor up and into the line but dont shift the empty last line
        for i in range(0,3):
            mlb.handle_up()
        for i in range(0,16):
            mlb.handle_right() 
        self.assertEqual(mlb.cpos_y_content, 15)
        self.assertEqual(mlb.cpos_x_content, 16)
        self.assertEqual(mlb.cpos_y_buffer, 3)
        self.assertEqual(mlb.cpos_x_buffer, 11)
        mlv: MultiLineView2 = MultiLineView2(content_lines=mlb.content, \
            cpos_y_content = mlb.cpos_y_content,  \
            cpos_x_content = mlb.cpos_x_content,  \
            view_height    = height,  \
            view_width     = width, \
            cpos_y_buffer  = mlb.cpos_y_buffer,  \
            cpos_x_buffer  = mlb.cpos_x_buffer)
        b = mlv.make_debug()
        dbg_cursor = mlv.debug_cursor_line
        buf = mlv.view_buffer
        expected =  [
            lines[12], 
            lines[13], 
            lines[14], 
            lines[15],
            lines[16],
            lines[17],
            ""
        ]
        expected_buffer = [ 
            "456789A12345",
            "456789A12345",
            "456789A12345",
            "456789A12345",
            "3456789A1234",
            "3456789A1234",
            ""
        ]
        self.assertEqual(b, expected)
        self.assertEqual(buf, expected_buffer)
        self.assertEqual(mlv.char_under_cursor, "5")
        self.assertEqual(mlv.view_height, 7)
        self.assertEqual(mlv.view_content_y_begin, 12)
        self.assertEqual(mlv.view_content_y_end, 18)
        self.assertEqual(mlv.view_buffer_y_begin, 0)
        self.assertEqual(mlv.view_buffer_y_end, 6)

    def test_multiline_view_4(self):
        height = 7
        width = 12
        local_lines = lines[0:6]
        self.assertEqual(len(local_lines), 6)
        mlb: MultiLineBuffer = MultiLineBuffer(lines=local_lines, height=height, width=width)
        # put the cursor after the last character on the last line - the last line is not empty
        mlb._cursor_set_at_end() 
        # move the cursor up and into the line but dont shift the empty last line
        for i in range(0,2):
            mlb.handle_up()
        for i in range(0,8):
            mlb.handle_left() 
        self.assertEqual(mlb.cpos_y_content, 3)
        self.assertEqual(mlb.cpos_x_content, 34)
        self.assertEqual(mlb.cpos_y_buffer, 4)
        self.assertEqual(mlb.cpos_x_buffer, 4)
        mlv: MultiLineView2 = MultiLineView2(content_lines=mlb.content, \
            cpos_y_content = mlb.cpos_y_content,  \
            cpos_x_content = mlb.cpos_x_content,  \
            view_height    = height,  \
            view_width     = width, \
            cpos_y_buffer  = mlb.cpos_y_buffer,  \
            cpos_x_buffer  = mlb.cpos_x_buffer)
        b = mlv.make_debug()
        dbg_cursor = mlv.debug_cursor_line
        buf = mlv.view_buffer
        expected =  [
            "Z",
            local_lines[0], 
            local_lines[1], 
            local_lines[2], 
            local_lines[3],
            local_lines[4],
            local_lines[5],
        ]
        expected_buffer = [ 
            "",
            "9C123456789D",
            "9C123456789D",
            "9C123456789D",
            "9C123456789D",
            "9C123456789D",
            "9C123456789D",
        ]
        self.assertEqual(b, expected)
        self.assertEqual(buf, expected_buffer)
        self.assertEqual(mlv.char_under_cursor, "3")
        self.assertEqual(mlv.view_height, 7)
        self.assertEqual(mlv.view_content_y_begin, 0)
        self.assertEqual(mlv.view_content_y_end, 5)
        self.assertEqual(mlv.view_buffer_y_begin, 1)
        self.assertEqual(mlv.view_buffer_y_end, 6)

    def test_multiline_view_5(self):
        height = 7
        width = 12
        local_lines = lines[0:6]
        self.assertEqual(len(local_lines), 6)
        mlb: MultiLineBuffer = MultiLineBuffer(lines=local_lines, height=height, width=width)
        # put the cursor after the last character on the last line - the last line is not empty
        mlb._cursor_set_after_end() 
        # # move the cursor up and into the line but dont shift the empty last line
        # for i in range(0,2):
        #     mlb.handle_up()
        # for i in range(0,8):
        #     mlb.handle_left() 
        self.assertEqual(mlb.cpos_y_content, 6)
        self.assertEqual(mlb.cpos_x_content, 0)
        self.assertEqual(mlb.cpos_y_buffer, 6)
        self.assertEqual(mlb.cpos_x_buffer, 0)
        mlv: MultiLineView2 = MultiLineView2(content_lines=mlb.content, \
            cpos_y_content = mlb.cpos_y_content,  \
            cpos_x_content = mlb.cpos_x_content,  \
            view_height    = height,  \
            view_width     = width, \
            cpos_y_buffer  = mlb.cpos_y_buffer,  \
            cpos_x_buffer  = mlb.cpos_x_buffer)
        b = mlv.make_debug()
        dbg_cursor = mlv.debug_cursor_line
        buf = mlv.view_buffer
        expected =  [
            local_lines[0], 
            local_lines[1], 
            local_lines[2], 
            local_lines[3],
            local_lines[4],
            local_lines[5],
            ""
        ]
        expected_buffer = [ 
            "0 123456789A",
            "1 123456789A",
            "2 123456789A",
            "3 123456789A",
            "4 123456789A",
            "5 123456789A",
            " ",
        ]
        self.assertEqual(b, expected)
        self.assertEqual(buf, expected_buffer)
        self.assertEqual(mlv.char_under_cursor, " ")
        self.assertEqual(mlv.view_height, 7)
        self.assertEqual(mlv.view_content_y_begin, 0)
        self.assertEqual(mlv.view_content_y_end, 6)
        self.assertEqual(mlv.view_buffer_y_begin, 0)
        self.assertEqual(mlv.view_buffer_y_end, 6)

    def test_multiline_view_6(self):
        height = 7
        width = 12
        local_lines = lines[0:6]
        self.assertEqual(len(local_lines), 6)
        mlb: MultiLineBuffer = MultiLineBuffer(lines=local_lines, height=height, width=width)
        # put the cursor after the last character on the last line - the last line is not empty
        mlb._cursor_set_after_end() 
        # move the cursor up and into the line but dont shift the empty last line
        for i in range(0,2):
            mlb.handle_up()
        for i in range(0,8):
            mlb.handle_left() 
        self.assertEqual(mlb.cpos_y_content, 4)
        self.assertEqual(mlb.cpos_x_content, 0)
        self.assertEqual(mlb.cpos_y_buffer, 4)
        self.assertEqual(mlb.cpos_x_buffer, 0)
        mlv: MultiLineView2 = MultiLineView2(content_lines=mlb.content, \
            cpos_y_content = mlb.cpos_y_content,  \
            cpos_x_content = mlb.cpos_x_content,  \
            view_height    = height,  \
            view_width     = width, \
            cpos_y_buffer  = mlb.cpos_y_buffer,  \
            cpos_x_buffer  = mlb.cpos_x_buffer)
        b = mlv.make_debug()
        dbg_cursor = mlv.debug_cursor_line
        buf = mlv.view_buffer
        expected =  [
            local_lines[0], 
            local_lines[1], 
            local_lines[2], 
            local_lines[3],
            local_lines[4],
            local_lines[5],
            ""
        ]
        expected_buffer = [ 
            "0 123456789A",
            "1 123456789A",
            "2 123456789A",
            "3 123456789A",
            "4 123456789A",
            "5 123456789A",
            "",
        ]
        self.assertEqual(b, expected)
        self.assertEqual(buf, expected_buffer)
        self.assertEqual(mlv.char_under_cursor, "4")
        self.assertEqual(mlv.view_height, 7)
        self.assertEqual(mlv.view_content_y_begin, 0)
        self.assertEqual(mlv.view_content_y_end, 6)
        self.assertEqual(mlv.view_buffer_y_begin, 0)
        self.assertEqual(mlv.view_buffer_y_end, 6)



if __name__ == '__main__':
    unittest.main()
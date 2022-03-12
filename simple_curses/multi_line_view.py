from typing import List, Set, Dict, Tuple, Optional
import string 


class MultiLineView2:
    def __init__(self, content_lines: List[str], cpos_y_content: int, cpos_x_content: int, view_height: int, view_width: int, cpos_y_buffer: int, cpos_x_buffer: int):
        tmp = cpos_y_content - cpos_y_buffer
        self.view_content_y_begin = tmp if tmp >= 0 else 0
        if tmp >= 0:
            self.view_content_y_begin = tmp
            self.view_buffer_y_begin = 0
        else:
            self.view_content_y_begin = 0
            self.view_buffer_y_begin = -tmp

        xtmp = cpos_x_content - cpos_x_buffer
        self.view_content_x_begin = xtmp if xtmp > 0 else 0
        view_content_x_end = 0
        self.content_lines = content_lines
        self.view_height = view_height
        self.view_width = view_width
        self.cpos_y_content = cpos_y_content
        self.cpos_y_buffer = cpos_y_buffer
        self.cpos_x_content = cpos_x_content
        self.cpos_x_buffer = cpos_x_buffer
        # calculate self.view_content_y_end by enumerating cases

        if self.view_content_y_begin > 0 and self.view_content_y_begin + view_height - 1 < len(content_lines):
            # case 1
            # content is larger than buffer
            # last line of content is on or past the last line of buffer
            # y cursor is somewhere in buffer on a real conttent line 
            self.view_content_y_end = self.view_content_y_begin + view_height - 1
            self.view_buffer_y_end = view_height - 1

        elif self.view_content_y_begin > 0 and  cpos_y_buffer == view_height - 1 and cpos_y_content == len(content_lines) and len(content_lines) >= view_height:
            # case 2
            # content is larger than buffer
            # last line of content is on 2nd last line of buffer
            # y cursor is on last line of buffer and on imaginery line of content at index len(content_lines)
            self.view_content_y_end = len(content_lines) 
            self.view_buffer_y_end = view_height - 1

        elif self.view_content_y_begin > 0 and cpos_y_buffer < view_height - 1 and self.view_content_y_begin + view_height - 1 == len(content_lines) and cpos_y_content < len(content_lines):
            # case 3
            # content is larger than buffer
            # last line of content is on 2nd last line of buffer
            # y_cursor is on a true content line
            self.view_content_y_end = len(content_lines) - 1
            self.view_buffer_y_end = view_height - 2
            
        elif self.view_content_y_begin == 0 and len(content_lines) < view_height and cpos_y_content < len(content_lines): # and cpos_y_buffer + (view_height - 1) - cpos_y_content == (view_height - 1):
            # case 4 - 
            # content is smaller than buffer
            # last line of content is on last line of buffer
            # y cursor is on a true content line sonewhere in the buffer
            self.view_content_y_end = len(content_lines) - 1
            self.view_buffer_y_end = view_height - 1

        elif self.view_content_y_begin == 0 and cpos_y_content == len(content_lines) and cpos_y_buffer == view_height - 1 and len(content_lines) <= view_height:
            # case 5
            # content is smaller than buffer
            # last line of content is on 2nd last line of buffer
            # y cursor is on last line of buffer and on imaginery line of content at index len(content_lines) 
            self.view_content_y_end = len(content_lines)
            self.view_buffer_y_end = view_height - 1
            
        elif self.view_content_y_begin == 0 and cpos_y_content < len(content_lines):
            # case 6
            # content is larger than buffer
            # last line of content is on 2nd last line of buffer
            # y_cursor is on a true content line
            self.view_content_y_end = len(content_lines) - 1
            self.view_buffer_y_end = view_height - 1
        else:
            raise RuntimeError("{}Invlid case".format(self.__class__.__name__))

        # in here need to calculate view_content_x_begin view_content_x_end view_buffer_x_begin view_content_x_end

        self.debug_cursor_line = self.make_cursor_debug_line()
        self.debug_buffer = self.make_debug()

        self.view_buffer = self.make_view_buffer()
        self.make_char_under_cursor()

    def make_char_under_cursor(self):
        """calculates the character that should be under the cursor and if necessary puts a blank there
        in the property self.view_buffer so that a user of this instance can index directly to the cursor
        position without worrying about index-out-of-range"""

        cursor_line = self.view_buffer[self.cpos_y_buffer]
        if cursor_line == "":
            self.char_under_cursor = " "
            self.view_buffer[self.cpos_y_buffer] += " "
        elif self.cpos_x_buffer == len(cursor_line):
            self.char_under_cursor = " "
            self.view_buffer[self.cpos_y_buffer] += " "
        elif self.cpos_x_buffer < len(cursor_line):
            self.char_under_cursor = cursor_line[self.cpos_x_buffer: self.cpos_x_buffer + 1]
        else:
            raise RuntimeError("cpos_y_buffer {} is too big".format(self.cpos_y_buffer))

    def make_view_buffer(self):
        """make an array with the same number of rows as the view buffer
        and where the array contains exactly what the view buffer should show"""
        buffer: List[str] = []
        for j in range(0, self.view_height):
            buffer.append("")
        bindex = self.view_buffer_y_begin
        for index in range(self.view_content_y_begin, self.view_content_y_end + 1):
            line  = self.content_lines[index]
            m = len(line) if len(line) < self.view_content_x_begin + self.view_width - 1 else self.view_content_x_begin + self.view_width - 1  
            buffer[bindex] = line[self.view_content_x_begin: m + 1]
            bindex += 1

        return buffer

    def make_debug(self):
        buffer: List[str] = []
        for j in range(0, self.view_height):
            buffer.append("Z")
        bindex = self.view_buffer_y_begin
        for index in range(self.view_content_y_begin, self.view_content_y_end + 1):
            line  = self.content_lines[index] if index < len(self.content_lines) else "W"
            buffer[bindex] = line
            bindex += 1

        return buffer

    def make_display_line(self):
        """Creates a line for the cursor to reside in. If necessay adds an extra space at the end"""
        raw_line = self.content_lines[self.cpos_y_content]
        if raw_line == "" and self.cpos_x_buffer > 0:
            raise RuntimeError("raw line is empty and x_begin is not zero")
        elif raw_line == "" and self.cpos_x_content == 0:
            return " "
        elif self.cpos_x_content == len(raw_line):
            return raw_line + EOSPAD
        elif self.cpos_x_content < len(raw_line):
            return raw_line
        else:
            raise RuntimeError("make_display_line - invalid curs_x")

    def make_cursor_debug_line(self):
        """makes a line that demonstrates where the cursor will be in the line - for debug only"""
        cursor_line = self.content_lines[self.cpos_y_content]
        if self.cpos_x_content == len(cursor_line):
            cursor_line = cursor_line + "X"
            self.view_content_x_end = len(cursor_line) - 1
        else:
            cursor_line = cursor_line[0: self.cpos_x_content] + "X" + cursor_line[self.cpos_x_content + 1: len(cursor_line)]
            self.view_content_x_end = len(cursor_line) - 1
        orig = self.content_lines[self.cpos_y_content] 
        ruler = "0123456789A123456789B123456789C123456789D"
        return [cursor_line, cursor_line[self.view_content_x_begin: self.view_content_x_end+1], orig, ruler ]


class MultiLineView:
    def __init__(self, lines, one_based_line_numbers, curs_y: int, curs_x: int, curs_char: str):
        self.paste_mode = False
        self.lines: List[str] = lines
        self.curs_y: int = curs_y
        self.curs_x: int = curs_x
        self.curs_char: str = curs_char
        self.one_based_line_numbers =[]
        for item in one_based_line_numbers:
            self.one_based_line_numbers.append(item) 
        self.cursor_line_debug: str = self._mk_cursor_line()


    def _mk_cursor_line(self):
        cline = self.lines[self.curs_y]
        if self.curs_x == len(cline):
            cline = cline + "X"
        else:
            cline = cline[0: self.curs_x] + "X" + cline[self.curs_x + 1: len(cline)]
        return cline


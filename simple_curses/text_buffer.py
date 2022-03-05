from asyncore import socket_map
from typing import List, Set, Dict, Tuple, Optional
import string 

# 
# TODO - there is still more cleanup of this code to be done
# TODO - the handling of the APPEND mode is poor
# TODO - should display self.width characters in edit mode only need the blank on the end whan appending


# insert a character into the self.content string at the given position
# does not modify any properties
def _string_insert_character(str, pos, ch):
    assert (pos >= 0 and pos <= len(str) and len(str) > 0)
    s1 = str
    s21 = s1[0: pos] + ch
    s22 = s1[pos: len(s1)]
    return s21 + s22

# delete a character from within the self.content string and return the new string
# does not modify any properties
def  _string_delete_character(str, pos):
    assert (pos >= 0 and pos <= len(str) and len(str) > 0)
    if pos == 0:
        return str[1: len(str)]
    s1 = str
    s21 = s1[0: pos]
    s22 = s1[pos + 1: len(s1)]
    return s21 + s22

def _string_split_at_pos(str, pos):
    pre = str[0: pos]
    post = str[pos: len(str)]
    return [pre, post]

def _list_split_at_line_pos(ar: List[str], line_index, char_index):
    p, s = _string_split_at_pos(ar[line_index], char_index)
    ar[line_index] = p
    ar.insert(line_index + 1, s)
    return ar

def _list_delete_by_index(ar, index):
    del ar[index]

# 
# This class provides  
# -     fixed width multi-line buffer that acts as a display window or view into an arbitary length array string,
# -     together with the position of a cursor within that buffer window.
# 
# Methods are provided for the buffer content and cursor position as a result of:
# -     appending characters
# -     backspacing to delete the last character
# -     up/down arrow keys for navigating within the array entries
# -     left and right arrow navigation within thestring
# -     deleting an internal character 
# 
class TextBuffer:
    STATE_APPENDING = 1
    STATE_EDITING = 2
    EOSPAD = " "
    def __init__(self, lines: List[str], height: int, width: int):

        self.state = self.STATE_APPENDING
        self.content = [""]

        # width of the display buffer
        self.width = width
        self.view_height = height

        # 
        # Next 4 properties specify the cursor position in the view buffer and in the 
        #  content array and current content array element
        # 
        # the current cursor position in the current line of the buffer
        self.cpos_x_buffer = 0
        # index of the current view line
        self.cpos_y_buffer = 0
        # cursor position in the content string element of the content array
        self.cpos_x_content = 0
        # index of the current array element
        self.cpos_y_content = 0

        # specifies the portion of the self.content array that will be displayed in
        # the view window or buffer
        self.view_y_begin = 0 # an index into self.content - the first view line
        self.view_y_end = 0   # an index into self.content - the last view line
        self.view_x_begin = 0 # an index into self.content[i] the first character to be displayed - 
        self.view_x_end = 0   # an index into all displayable lines of self.content - the last character to be displayed

        # The string that will appear in the buffer window
        self.display_string = ""
        # self._compute_display_string()

        for line in lines:
            self.append_line(line)


    def _incr_cpos_x_buffer(self):
        self.cpos_x_buffer = self.cpos_x_buffer + 1 if self.cpos_x_buffer < self.width - 1 else self.cpos_x_buffer

    def _decr_cpos_x_buffer(self):
        self.cpos_x_buffer = self.cpos_x_buffer - 1 if self.cpos_x_buffer > 0 else self.cpos_x_buffer

    def _incr_cpos_x_content(self):
        self.cpos_x_content = self.cpos_x_content + 1 if self.cpos_x_content < len(self.content[self.cpos_y_content]) else len(self.content[self.cpos_y_content])

    def _decr_cpos_x_content(self):
        self.cpos_x_content = self.cpos_x_content - 1 if self.cpos_x_content > 0 else self.cpos_x_content

    def _incr_cpos_y_content(self):
        self.cpos_y_content = self.cpos_y_content + 1 if self.cpos_y_content < len(self.content) - 1 else len(self.content) - 1 

    def _decr_cpos_y_content(self):
        self.cpos_y_content = self.cpos_y_content - 1 if self.cpos_y_content > 0 else 0 

    def _incr_cpos_y_buffer(self):
        self.cpos_y_buffer = self.cpos_y_buffer + 1 if self.cpos_y_buffer < self.view_height - 1 else self.view_height - 1 

    def _decr_cpos_y_buffer(self):
        self.cpos_y_buffer = self.cpos_y_buffer - 1 if self.cpos_y_buffer > 0 else 0 


    # returns true if the content is larger than the buffer window in append mode
    def _content_overflow_append(self):
        tmp = len(self.content[self.cpos_y_content] + self.EOSPAD) > (self.width - 1)
        return tmp

    # returns true if the content is larger than the buffer window in edit mode
    def _content_overflow_edit(self):
        tmp = len(self.content[self.cpos_y_conttent]) > (self.width - 1)
        return tmp

    # convert a buffer position to a position in the content string
    def _bufpos_to_contentpos(self, bpos):
        return self.cpos_x_content + (bpos - self.cpos_x_buffer)

    # cursor is over the contents first character
    def _cursor_at_content_start(self):
        return self.cpos_x_content == 0

    # cursor is over the content last character
    def cursor_at_content_end(self):
        return self.cpos_content == len(self.content[self.cpos_y_content])

    # cursor is immerdiately to the right of the contents last character 
    def _cursor_after_content_end(self):
        return self.cpos_content == len(self.content[self.cpos_y_content])

    # the end position in the content string of the last+1 buffer chararcer
    def _bufferend_to_contentpos(self):
        leng = len(self.content[self.cpos_y_content])
        max_stop = (self.view_x_begin + (self.width) - 1)
        stop_pos = leng if (leng <= max_stop) else max_stop
        return stop_pos

    # computes the range of lines from self.content that will be displayed
    # represents this range as self.view_begin_y and self.view_end_y 
    def _compute_y_view(self):
        self.view_y_begin = self.cpos_y_content - self.cpos_y_buffer
        last = len(self.content) - 1
        tmp = self.view_y_begin + self.view_height - 1
        self.view_y_end = tmp if tmp < last else last

    # computes the portion of a string (element of self.content) that will be displayed
    # assumption - the line is NOT the line holding the cursor
    def _compute_line_view(self, i):
        if i == self.cpos_y_content:
            self._compute_display_string()
            tmp = self.display_string
            return tmp
        else:
            tmp = self.content[i][self.view_x_begin: len(self.content[i])]
            return tmp

    def _compute_display_string(self):
        start = self.cpos_x_content - self.cpos_x_buffer

        # case0 there will be more than 1 unfilled slot at the end of the buffer
        case0 = start + (self.width - 1) > len(self.content[self.cpos_y_content])
        # case1 there will be exactly 1 unfilled slot at the end of the buffer
        case1 = start + (self.width - 1) == len(self.content[self.cpos_y_content])
        # casae2 there will be zero unfilled slots at the end of the buffer
        case2 = start + (self.width - 1) <= len(self.content[self.cpos_y_content]) - 1
        if case0 or case1:
            # self.display_string = (self.content) [start: start + (self.width - 1)] + self.EOSPAD
            if start + self.width >= len(self.content[self.cpos_y_content]):
                if start + self.cpos_x_buffer >= len(self.content[self.cpos_y_content]):
                    self.display_string = (self.content[self.cpos_y_content]) [start: start + len(self.content[self.cpos_y_content])] + self.EOSPAD
                else:
                    self.display_string = (self.content[self.cpos_y_content]) [start: start + len(self.content[self.cpos_y_content])]
            else:
                self.display_string = (self.content[self.cpos_y_content]) [start: start + self.width]
        elif case2:
                self.display_string = (self.content[self.cpos_y_content]) [start: start + (self.width)]

        # if(self.display_string != self.display_string):
        #     print("display string mismatch display_string: [{}] display_string: [{}] cpos_buffer: {}".format(self.display_string, self.display_string, self.cpos_buffer))
        #     print("_compute_display_string case0: {} case1 : {} case2 : {}".format(case0, case1, case2))
        # if self.cpos_buffer > len(self.display_string) - 1:
        #     print("_compute_display_string: no character under cursor display_string: [{}] len(display_string): {} cpos_buffer {}".format(self.display_string, len(self.display_string), self.cpos_buffer))

        # self.display_string = self.content[self.view_x_begin: self._bufferend_to_contentpos()] + self.EOSPAD

    # insert a character into the self.content string at the given position
    # does not modify any properties
    def _content_insert_character(self, pos, ch):
        if self.state == self.STATE_APPENDING:
            assert False, "content insert character only for edit mode"

        assert (pos >= 0 and pos <= len(self.content[self.cpos_y_content]) and len(self.content[self.cpos_y_content]) > 0)
        return _string_insert_character(self.content[self.cpos_y_content], pos, ch)
    
    # delete a character from within the self.content string and return the new string
    # does not modify any properties
    def  _content_remove_character(self, pos):
        if self.state == self.STATE_APPENDING:
            assert False, "content remove character only for edit mode"
        return _string_delete_character(self.content[self.cpos_y_content], pos)

    def get_view(self):
        view = []
        self._compute_y_view()
        for i in range(self.view_y_begin, self.view_y_end + 1):
            s = self._compute_line_view(i)
            view.append(s)
        return view

    def handle_newline(self):
        '''the return key will split a line at the cursor positon and put the portion of the line after the cursor
        into a new next line.
        The cursor position will be updated to the start of the next line and the buffer position will move down '''
        self.content = _list_split_at_line_pos(self.content, self.cpos_y_content, self.cpos_x_content)
        self._incr_cpos_y_content()
        self._incr_cpos_y_buffer()
        self.cpos_x_content = 0
        self.cpos_x_buffer = 0
        self._compute_y_view()

    def handle_up(self):
        self._decr_cpos_y_content()
        self._decr_cpos_y_buffer()
        self._compute_y_view()

    def handle_down(self):
        self._incr_cpos_y_content()
        self._incr_cpos_y_buffer()
        self._compute_y_view()

    def append_line(self, line):
        if len(self.content) == 1 and self.content[0] == "":
            self.content[0] = line
        elif len(self.content) == 0:
            self.content.append(line)
        else:
            self.content.append(line)
            self._incr_cpos_y_content()
            self._incr_cpos_y_buffer()
        self._compute_y_view()

    def handle_add_line(self, line):
        pass
    def handle_delete_line(self):
        """delete the line that under the cursor and move the cursor to the same position (or as close as possible)
        in the following line - if no following line move to the now last line """
        del self.content[self.cpos_y_content]
        if self.cpos_y_content >= len(self.content):
            self.cpos_y_content = len(self.content) - 1
        self.cpos_x_content = 0
        self.cpos_x_buffer = 0 

    # handle a new non editing and non navigation character. Add to the buffer and update state variables
    def handle_character(self, ch):
        
        if self.state == self.STATE_APPENDING:
            assert (self.cpos_x_content == len(self.content[self.cpos_y_content]))
            self.content += ch
            if self._content_overflow_append():
                self.cpos_x_buffer = self.width - 1
                self.cpos_x_content = len(self.content[self.cpos_y_content])
            else:
                self.cpos_x_buffer = len(self.content[self.cpos_y_content] + self.EOSPAD) - 1
                self.cpos_x_content = len(self.content[self.cpos_y_content] + self.EOSPAD) - 1 
            self._compute_display_string()
        else:
            pos = self.cpos_x_content
            self._incr_cpos_content()
            self._incr_cpos_buffer()
            self.content[self.cpos_y_content] = self._content_insert_character(pos, ch)
            self._compute_display_string()

    # handle a backspace character. Delete the character on the left of the cursor
    def handle_backspace(self):
        if self.state == self.STATE_APPENDING:
            self.content[self.cpos_y_content] = self.content[self.cpos_y_content][0: len(self.content[self.cpos_y_content]) - 1]
            if self._content_overflow_append():
                self.cpos_x_buffer = self.width - 1
                self.cpos_x_content = len(self.content[self.cpos_y_content])
            else:
                self.cpos_x_buffer = len(self.content[self.cpos_y_content]) 
                self.cpos_x_content = len(self.content[self.cpos_y_content])

            self._compute_display_string()
        else:
            if not self._cursor_at_content_start():
                del_pos = self.cpos_content - 1
                self.content[self.cpos_y_content] = self._content_remove_character(del_pos)

                if self.cpos_x_buffer == self.cpos_x_content:
                    self._decr_cpos_buffer()
                self._decr_cpos_content()
                self._compute_display_string()

            if len(self.content[self.cpos_y_content]) == 0:
                self.state = self.STATE_APPENDING

    # handle delete - character under cursor
    def handle_delete(self):
        if self.state == self.STATE_APPENDING:
            return
        if (self.cpos_x_buffer == self.width - 1) and (self.view_x_begin + self.width) == len(self.content[self.cpos_y_content]):
            pass
        else:
            if len(self.content[self.cpos_y_content]) == 0:
                return
            pos = self.cpos_x_content
            self.content[self.cpos_y_content] = self._content_remove_character(pos)
            if len(self.content[self.cpos_y_content]) == 0:
                self.state  = self.STATE_APPENDING
                self._compute_display_string()
            else:
                self._compute_display_string()

    
    # handle left arrow - 
    def handle_left(self):
        if self.state == self.STATE_APPENDING:
            self.state = self.STATE_EDITING 
        self._decr_cpos_buffer()
        self._decr_cpos_content()
        self._compute_display_string()

   
    # handle right arrow key
    def handle_right(self):
        if self.state == self.STATE_APPENDING:
            return
        self._incr_cpos_buffer()
        self._incr_cpos_content()
        self._compute_display_string()

        if self._cursor_after_content_end():
            self.state = self.STATE_APPENDING

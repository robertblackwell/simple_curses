from hashlib import new
from typing import List, Set, Dict, Tuple, Optional
import string
from .multi_line_view import MultiLineView2


#
# TODO - there is still more cleanup of this code to be done
# TODO - the handling of the APPEND mode is poor
# TODO - should display self.width characters in edit mode only need the blank on the end whan appending


# insert a character into the self.content string at the given position
# does not modify any properties
def _string_insert_character(str, pos, ch):
    assert (0 <= pos <= len(str) and len(str) >= 0)
    s1 = str
    s21 = s1[0: pos] + ch
    s22 = s1[pos: len(s1)]
    return s21 + s22


# delete a character from within the self.content string and return the new string
# does not modify any properties
def _string_delete_character(str, pos):
    assert (0 <= pos <= len(str) and len(str) > 0)
    if pos == 0:
        return str[1: len(str)]
    s1 = str
    s21 = s1[0: pos]
    s22 = s1[pos + 1: len(s1)]
    return s21 + s22


def _string_split_at_pos(astring, pos):
    pre = astring[0: pos]
    post = astring[pos: len(astring)]
    return [pre, post]


def _list_split_at_line_pos(ar: List[str], line_index, char_index):
    p, s = _string_split_at_pos(ar[line_index], char_index)
    ar[line_index] = p
    ar.insert(line_index + 1, s)
    return ar


def _list_delete_by_index(ar, index):
    del ar[index]


EOSPAD = " "


def join_lines(lines: List[str], index: int):
    """
    lines is an array of strings.
    Return a new array with the lines at index-1 and index comnined into a single entry
    """
    if index == 0:
        raise RuntimeError("join_lines index must not be zero")
    s_index = lines[index]
    s_index_1 = lines[index - 1]
    lines2 = lines[0: index - 1]
    lines2.append(s_index_1 + s_index)
    for lin in lines[index + 1: len(lines)]:
        lines2.append(lin)
    return lines2


class MultiLineBuffer:
    """
    This class provides  
    -   fixed width, fixed length multi-line buffer that acts as a display window or view into an arbitary length array of string.
    -   it maintains two cursor positions:
            - cpos_y_content, cpos_x_content is the position of the cursor within the array of strings
            - cpos_y_buffer, cpos_x_buffer is the position within the fixed width, fixed height display buffer

    -   There is an auxilliary class MultiLineView which uses the two cursor positions to compute
        the text that should be displayed by a MultiLineWidget 
     
    Methods are provided to calculate the buffer content and cursor positions as a result of:
    -     appending/inserting characters
    -     backspacing to delete the character preceeding
    -     delete key to delete the character under the cursor
    -     up/down arrow keys for navigating between lines in the array of strings
    -     left and right arrow navigation within a single line
     
    """

    EOSPAD = " "

    def __init__(self, lines: List[str], height: int, width: int):

        self.content = [""]
        self.width = width
        self.view_height = height
        self.cpos_x_buffer = 0
        self.cpos_y_buffer = 0
        self.cpos_x_content = 0
        self.cpos_y_content = 0

        for line in lines:
            self.append_line(line)

    ############################################################################################################
    # increment descrement -
    # These functions increment and decrement the cursor offsets without allowing them to run
    # off the end of the self.content or the view window
    ############################################################################################################
    def _incr_cpos_x_buffer(self):
        self.cpos_x_buffer = self.cpos_x_buffer + 1 if self.cpos_x_buffer < self.width - 1 else self.cpos_x_buffer

    def _decr_cpos_x_buffer(self):
        self.cpos_x_buffer = self.cpos_x_buffer - 1 if self.cpos_x_buffer > 0 else self.cpos_x_buffer

    def _incr_cpos_x_content(self):
        self.cpos_x_content = self.cpos_x_content + 1 if self.cpos_x_content < len(
            self.content[self.cpos_y_content]) else len(self.content[self.cpos_y_content])

    def _decr_cpos_x_content(self):
        self.cpos_x_content = self.cpos_x_content - 1 if self.cpos_x_content > 0 else self.cpos_x_content

    def _incr_cpos_y_content(self):
        self.cpos_y_content = self.cpos_y_content + 1 if self.cpos_y_content < len(self.content) - 1 else len(
            self.content) - 1

    def _decr_cpos_y_content(self):
        self.cpos_y_content = self.cpos_y_content - 1 if self.cpos_y_content > 0 else 0

    def _incr_cpos_y_buffer(self):
        self.cpos_y_buffer = self.cpos_y_buffer + 1 if self.cpos_y_buffer < self.view_height - 1 else self.view_height - 1

    def _decr_cpos_y_buffer(self):
        self.cpos_y_buffer = self.cpos_y_buffer - 1 if self.cpos_y_buffer > 0 else 0

    ############################################################################################################
    # cursor manipulation - These are primitive operations on the cpos_y_ and cpos_x values
    ############################################################################################################
    def _cursor_x_set_to_zero(self):
        """makes both cpos_x offsets point to the start of the current line """
        self.cpos_x_content = 0
        self.cpos_x_buffer = 0

    def _update_cursor_x(self):
        """called whenever the cpos_y values are updated to ensure the cpos_x values are consistent with the width of the buffer
        used by the up arrow and down arrow processing to ensure
        the x position of the cursor is always valid regardless of the length of the current line"""
        old_cpos_x = self.cpos_x_content
        len_new_line = len(self.content[self.cpos_y_content])
        if self.cpos_x_content >= len_new_line:
            self.cpos_x_content = len_new_line
            change_cpos_x = self.cpos_x_content - old_cpos_x
            self.cpos_x_buffer += change_cpos_x
        else:
            pass

    ############################################################################################################
    # content manipulation for insert and delete of content characters
    ############################################################################################################
    def _content_insert_character(self, pos, ch):
        """ insert a character into the self.content string at the given position
        does not modify any properties"""
        if self._is_cursor_after_line_end():
            assert False, "content insert character only for edit mode"

        assert (0 <= pos <= len(self.content[self.cpos_y_content]) and len(
            self.content[self.cpos_y_content]) >= 0)
        return _string_insert_character(self.content[self.cpos_y_content], pos, ch)

    def _content_remove_character(self, pos):
        """# delete a character from within the self.content string and return the new string
        does not modify any properties"""
        if self._is_cursor_after_line_end():
            assert False, "content remove character only for edit mode"
        return _string_delete_character(self.content[self.cpos_y_content], pos)

    ############################################################################################################
    # cursor and content condition tests - test various aspects of the cursor position and the content relative
    # to the view window
    ############################################################################################################
    def _is_content_overflow_append(self):
        """returns true if the current line is widther than the buffer window in append mode"""
        tmp = len(self.content[self.cpos_y_content] + self.EOSPAD) > (self.width - 1)
        return tmp

    # returns true if the content is larger than the buffer window in edit mode
    # def _is_content_overflow_edit(self):
    #     tmp = len(self.content[self.cpos_y_content]) > (self.width - 1)
    #     return tmp

    def _is_cursor_at_line_start(self):
        """# cursor is over the contents first character"""
        return self.cpos_x_content == 0

    def _is_cursor_at_line_end(self):
        """cursor is over the current lines last character"""
        return self.cpos_x_content == len(self.content[self.cpos_y_content]) - 1

    def _is_cursor_after_line_end(self):
        """cursor is immerdiately to the right of the current lines last character """
        return self.cpos_x_content == len(self.content[self.cpos_y_content])

    def _is_cursor_at_last_line(self):
        """Is the cursor on the last line"""
        return self.cpos_y_content == len(self.content) - 1

    def _is_cursor_at_empty_line(self):
        """Is the cursor on an empty line"""
        return self.content[self.cpos_y_content] == ""
    ##############################################################################
    # utility methods for back space and delete
    ##############################################################################
    
    def content_is_single_blank_line(self) -> bool:
        return len(self.content) == 0 or (len(self.content) == 1 and len(self.content[0]) == 0)

    def current_line_is_blank_and_not_last(self) -> bool:
        return self._is_cursor_at_empty_line() and not self._is_cursor_at_last_line()

    def current_line_is_blank_and_last(self) -> bool:
        return self.cpos_y_content == len(self.content) - 1 and self.content[len(self.content)-1] == ""

    def current_line_is_blank_and_first(self) -> bool:
        return self.cpos_y_content == 0 and self.content[0] == ""

    def current_line_remove_last_char(self) -> None:
        self.content[self.cpos_y_content] = self.content[self.cpos_y_content][
                                            0: len(self.content[self.cpos_y_content]) - 1]
    def remove_last_line(self) -> None:
        self.content = self.content[0: self.cpos_y_content]

    def remove_current_line(self) -> None:
        self.content.pop(self.cpos_y_content)

    def set_cursor_x_eol(self) -> None:
        if self._is_content_overflow_append():
            self.cpos_x_buffer = self.width - 1
            self.cpos_x_content = len(self.content[self.cpos_y_content])
        else:
            self.cpos_x_buffer = len(self.content[self.cpos_y_content])
            self.cpos_x_content = len(self.content[self.cpos_y_content])

    def set_cursor_at_end_of_previous_line(self) -> None:
        self._decr_cpos_y_content()
        self._decr_cpos_y_buffer()
        # self.cpos_y_content = self.cpos_y_content - 1
        # self.cpos_y_buffer = self.cpos_y_buffer - 1
        self.set_cursor_x_eol()
    ##############################################################################
    # END utility methods for back space and delete
    ##############################################################################

    ############################################################################################################
    # get_view
    ############################################################################################################
    def clear(self):
        self.content = [""]
        self.cpos_x_buffer = 0
        self.cpos_y_buffer = 0
        self.cpos_x_content = 0
        self.cpos_y_content = 0

    def get_value(self):
        return self.content

    def get_view(self) -> MultiLineView2:
        return MultiLineView2(
            content_lines=self.content,
            cpos_y_content=self.cpos_y_content,
            cpos_x_content=self.cpos_x_content,
            view_height=self.view_height,
            view_width=self.width,
            cpos_y_buffer=self.cpos_y_buffer,
            cpos_x_buffer=self.cpos_x_buffer,
            )

    ############################################################################################################
    # handlers for different character input
    ############################################################################################################

    def handle_newline(self):
        """the return key will split a line at the cursor positon and put the portion of the line after the cursor
        into a new next line.
        The cursor position will be updated to the start of the next line and the buffer position will move down 
        and the buffer will go to state STATE_EDIT"""
        if self._is_cursor_after_line_end():
            if self.cpos_y_content == len(self.content) - 1:
                self.content.append("")
            else:
                self.content.insert(self.cpos_y_content + 1,"")
            # pref = self.content[0: self.cpos_y_content] 
            # postf = self.content[self.cpos_y_content]
            # self.content = pref + [""] + postf
            self._incr_cpos_y_content()
            self._incr_cpos_y_buffer()
            self._cursor_x_set_to_zero()
        else:
            self.content = _list_split_at_line_pos(self.content, self.cpos_y_content, self.cpos_x_content)
            self._incr_cpos_y_content()
            self._incr_cpos_y_buffer()
            self._cursor_x_set_to_zero()

    def handle_up(self):
        self._decr_cpos_y_content()
        self._decr_cpos_y_buffer()
        self._update_cursor_x()

    def handle_down(self):
        self._incr_cpos_y_content()
        self._incr_cpos_y_buffer()
        self._update_cursor_x()

    def append_line(self, line):
        if len(self.content) == 1 and self.content[0] == "":
            self.content[0] = line
        elif len(self.content) == 0:
            self.content.append(line)
        else:
            self.content.append(line)
            self._incr_cpos_y_content()
            self._incr_cpos_y_buffer()
        self._cursor_x_set_to_zero()

    def handle_add_line(self, line):
        pass

    def handle_delete_line(self):
        """delete the line that under the cursor and move the cursor to the same position (or as close as possible)
        in the following line - if no following line move to the now last line """
        del self.content[self.cpos_y_content]
        if self.cpos_y_content >= len(self.content):
            self.cpos_y_content = len(self.content) - 1
        self._cursor_x_set_to_zero()

    # handle a new non editing and non navigation character. Add to the buffer and update state variables
    def handle_character(self, ch):
        if self._is_cursor_after_line_end():
            self.content[self.cpos_y_content] += ch
        else:
            self.content[self.cpos_y_content] = self._content_insert_character(self.cpos_x_content, ch)
        self._incr_cpos_x_content()
        self._incr_cpos_x_buffer()


    # handle a backspace character. Delete the character on the left of the cursor
    def handle_backspace(self):

        if self._is_cursor_after_line_end():
            if self.content_is_single_blank_line() or self.current_line_is_blank_and_first():
                return
            elif self.current_line_is_blank_and_not_last():
                self.remove_current_line()
                self.set_cursor_at_end_of_previous_line()
            elif self.current_line_is_blank_and_last():
                self.remove_last_line()
                self.set_cursor_at_end_of_previous_line()
            else: # current line is not blank
                self.current_line_remove_last_char()
                self.set_cursor_x_eol()
        else:
            if self._is_cursor_at_line_start():
                if self.cpos_y_content == 0:
                    pass
                else:
                    len_previous_line = len(self.content[self.cpos_y_content - 1])
                    self.content = join_lines(self.content, self.cpos_y_content)
                    self._decr_cpos_y_content()
                    self._decr_cpos_y_buffer()
                    # self._update_cursor_x()
                    self.cpos_x_content = len_previous_line
                    self.cpos_x_buffer = self.cpos_x_content if self.cpos_x_content < self.width else self.width - 1 
                    # self.cpos_x_buffer = len_previous_line
            else:
                del_pos = self.cpos_x_content - 1
                self.content[self.cpos_y_content] = self._content_remove_character(del_pos)
                if self.cpos_x_buffer == self.cpos_x_content:
                    self._decr_cpos_x_buffer()
                self._decr_cpos_x_content()

    # handle delete - character under cursor
    def handle_delete(self):
        if self._is_cursor_after_line_end():
            if self.content_is_single_blank_line():
                return
            elif self.current_line_is_blank_and_last():
                return
            elif self.current_line_is_blank_and_not_last():
                self.remove_current_line()
            else: # current line is not blank and cursor is after last character
                if self._is_cursor_at_last_line():
                    return
                else:
                    self.content = join_lines(self.content, self.cpos_y_content + 1)
        else:
            self.content[self.cpos_y_content] = _string_delete_character(self.content[self.cpos_y_content], self.cpos_x_content)

    # handle left arrow -
    def handle_left(self):
        """@TODO should move to previous line from start of line"""
        self._decr_cpos_x_buffer()
        self._decr_cpos_x_content()

    # handle right arrow key
    def handle_right(self):
        """@TODO should go to next line after end of current line"""
        if self._is_cursor_after_line_end():
            return
        self._incr_cpos_x_buffer()
        self._incr_cpos_x_content()


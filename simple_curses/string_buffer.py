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

# 
# This class provides  
# -     fixed width buffer that acts as a display window or view into an arbitory length string,
# -     together with the position of a cursor within that buffer window.
# 
# Methods are provided for the buffer content and cursor position as a result of:
# -     appending characters
# -     backspacing to delete the last character
# -     left and right arrow navigation within the string
# -     deleting an internal character 
# 
class StringBuffer:
    STATE_APPENDING = 1
    STATE_EDITING = 2
    EOSPAD = " "
    def __init__(self, str, width):
        self.state = self.STATE_APPENDING
        self.content = ""

        # width of the display buffer
        self.width = width
        # the current cursor position in the buffer
        self.cpos_buffer = 0
        # cursor position in the content string
        self.cpos_content = 0

        # position of first display character in the self.content string
        self.start_display_string = 0
        # The string that will appear in the buffer window
        self.display_string = ""
        self._compute_display_string()

        for c in str:
            self.handle_character(c)

    # tests the invariant between cpos_buffer, cpos_content and start_display_string
    def invariant(self):
        assert (self.start_display_string + self.cpos_buffer == self.cpos_content)

    def clear(self):
        self.cpos_content = 0
        self.cpos_buffer = 0
        self.display_string = ""
        self.content = ""
        self._compute_display_string()

    def _incr_cpos_buffer(self):
        self.cpos_buffer = self.cpos_buffer + 1 if self.cpos_buffer < self.width - 1 else self.cpos_buffer

    def _decr_cpos_buffer(self):
        self.cpos_buffer = self.cpos_buffer - 1 if self.cpos_buffer > 0 else self.cpos_buffer

    def _incr_cpos_content(self):
        self.cpos_content = self.cpos_content + 1 if self.cpos_content < len(self.content) else len(self.content)

    def _decr_cpos_content(self):
        self.cpos_content = self.cpos_content - 1 if self.cpos_content > 0 else self.cpos_content

    # returns true if the content is larger than the buffer window in append mode
    def _content_overflow_append(self):
        tmp = len(self.content + self.EOSPAD) > (self.width - 1)
        return tmp

    # returns true if the content is larger than the buffer window in edit mode
    def _content_overflow_edit(self):
        tmp = len(self.content) > (self.width - 1)
        return tmp

    # convert a buffer position to a position in the content string
    def _bufpos_to_contentpos(self, bpos):
        return self.cpos_content + (bpos - self.cpos_buffer)

    # cursor is over the contents first character
    def _cursor_at_content_start(self):
        return self.cpos_content == 0

    # cursor is over the content last character
    def cursor_at_content_end(self):
        return self.cpos_content == len(self.content)

    # cursor is immerdiately to the right of the contents last character 
    def _cursor_after_content_end(self):
        return self.cpos_content == len(self.content)

    # the end position in the content string of the last+1 buffer chararcer
    def _bufferend_to_contentpos(self):
        leng = len(self.content)
        max_stop = (self.start_display_string + (self.width) - 1)
        stop_pos = leng if (leng <= max_stop) else max_stop
        return stop_pos
        # self.display_string = self.content[self.start_display_string: stop_pos] + self.EOSPAD

    def _compute_display_string(self):
        start = self.cpos_content - self.cpos_buffer

        # case0 there will be more than 1 unfilled slot at the end of the buffer
        case0 = start + (self.width - 1) > len(self.content)
        # case1 there will be exactly 1 unfilled slot at the end of the buffer
        case1 = start + (self.width - 1) == len(self.content)
        # casae2 there will be zero unfilled slots at the end of the buffer
        case2 = start + (self.width - 1) <= len(self.content) - 1
        if case0 or case1:
            # self.display_string = (self.content) [start: start + (self.width - 1)] + self.EOSPAD
            if start + self.width >= len(self.content):
                if start + self.cpos_buffer >= len(self.content):
                    self.display_string = (self.content) [start: start + len(self.content)] + self.EOSPAD
                else:
                    self.display_string = (self.content) [start: start + len(self.content)]
            else:
                self.display_string = (self.content) [start: start + self.width]
        elif case2:
                self.display_string = (self.content) [start: start + (self.width)]

        # if(self.display_string != self.display_string):
        #     print("display string mismatch display_string: [{}] display_string: [{}] cpos_buffer: {}".format(self.display_string, self.display_string, self.cpos_buffer))
        #     print("_compute_display_string case0: {} case1 : {} case2 : {}".format(case0, case1, case2))
        # if self.cpos_buffer > len(self.display_string) - 1:
        #     print("_compute_display_string: no character under cursor display_string: [{}] len(display_string): {} cpos_buffer {}".format(self.display_string, len(self.display_string), self.cpos_buffer))

        # self.display_string = self.content[self.start_display_string: self._bufferend_to_contentpos()] + self.EOSPAD

    # insert a character into the self.content string at the given position
    # does not modify any properties
    def _content_insert_character(self, pos, ch):
        if self.state == self.STATE_APPENDING:
            assert False, "content insert character only for edit mode"

        assert (pos >= 0 and pos <= len(self.content) and len(self.content) > 0)
        return _string_insert_character(self.content, pos, ch)
    
    # delete a character from within the self.content string and return the new string
    # does not modify any properties
    def  _content_remove_character(self, pos):
        if self.state == self.STATE_APPENDING:
            assert False, "content remove character only for edit mode"
        return _string_delete_character(self.content, pos)

    # handle a new non editing and non navigation character. Add to the buffer and update state variables
    def handle_character(self, ch):
        
        if self.state == self.STATE_APPENDING:
            assert (self.cpos_content == len(self.content))
            self.content += ch
            if self._content_overflow_append():
                self.cpos_buffer = self.width - 1
                self.cpos_content = len(self.content)
            else:
                self.cpos_buffer = len(self.content + self.EOSPAD) - 1
                self.cpos_content = len(self.content + self.EOSPAD) - 1 
            self._compute_display_string()
        else:
            pos = self.cpos_content
            self._incr_cpos_content()
            self._incr_cpos_buffer()
            self.content = self._content_insert_character(pos, ch)
            self._compute_display_string()

    # handle a backspace character. Delete the character on the left of the cursor
    def handle_backspace(self):
        if self.state == self.STATE_APPENDING:
            self.content = self.content[0: len(self.content) - 1]
            if self._content_overflow_append():
                self.cpos_buffer = self.width - 1
                self.cpos_content = len(self.content)
            else:
                self.cpos_buffer = len(self.content) 
                self.cpos_content = len(self.content)

            self._compute_display_string()
        else:
            if not self._cursor_at_content_start():
                del_pos = self.cpos_content - 1
                self.content = self._content_remove_character(del_pos)

                if self.cpos_buffer == self.cpos_content:
                    self._decr_cpos_buffer()
                self._decr_cpos_content()
                self._compute_display_string()

            if len(self.content) == 0:
                self.state = self.STATE_APPENDING

    # handle delete - character under cursor
    def handle_delete(self):
        if self.state == self.STATE_APPENDING:
            return
        if (self.cpos_buffer == self.width - 1) and (self.start_display_string + self.width) == len(self.content):
            pass
        else:
            if len(self.content) == 0:
                return
            pos = self.cpos_content
            self.content = self._content_remove_character(pos)
            if len(self.content) == 0:
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

import time
import sys
import curses
import curses.textpad
import time
import string

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
        # position of first display character in the self.content string
        self.start_display_string = 0
        # The string that will appear in the buffer window
        self.display_string = ""

        for c in str:
            self.handle_character(c)

    # returns true if the content is larger than the buffer window in append mode
    def content_overflow_append(self):
        tmp = len(self.content + self.EOSPAD) > (self.width - 1)
        return tmp

    # returns true if the content is larger than the buffer window in edit mode
    def content_overflow_edit(self):
        tmp = len(self.content) > (self.width - 1)
        return tmp


    # calcs the index position of the cursor in the full content string
    def cursor_pos_in_content(self):
        if len(self.content) == 0 :
            return 0
        else:
            tmp = self.start_display_string + self.cpos_buffer
            return tmp

    # cursor is over the contents first character
    def cursor_at_content_start(self):
        return self.cursor_pos_in_content() == 0

    # cursor is over the content last character
    def cursor_at_content_end(self):
        return self.cursor_pos_in_content() == len(self.content)

    # cursor is immerdiately to the right of the contents last character 
    def cursor_after_content_end(self):
        return self.cursor_pos_in_content() == len(self.content)
    
    #
    # calculate the display string, depends on 
    #   -   self.state
    #   -   self.content
    #   -   self.EOSPAD
    #   -   self.start_display_string
    #   -   self.width
    #
    # Does not modify any properties
    #
    def calc_display_string(self):
        if self.state == self.STATE_APPENDING:
            if self.content_overflow_append:
                return (self.content + self.EOSPAD)[self.start_display_string, self.width - 1]
            else:
                return (self.content + self.EOSPAD)[self.start_display_string, len(self.content + self.EOSPAD)]
        else:
            if self.content_overflow_edit():
                st = self.start_display_string
                last = st + self.width - 1
                return (self.content)[self.start_display_string: last]
            else:
                return (self.content)[self.start_display_string: len(self.content)]
    

    # insert a character into the self.content string at the given position
    # does not modify any properties
    def content_insert_character(self, pos, ch):
        if self.state == self.STATE_APPENDING:
            assert False, "content insert character only for edit mode"

        assert (pos >= 0 and pos <= len(self.content) and len(self.content) > 0)
        return _string_insert_character(self.content, pos, ch)
    
    # delete a character from within the self.content string and return the new string
    # does not modify any properties
    def  content_remove_character(self, pos):
        if self.state == self.STATE_APPENDING:
            assert False, "content remove character only for edit mode"
        return _string_delete_character(self.content, pos)

    # handle a new non  editing and non navigation character. Add to the buffer and update state variables
    # 
    def handle_character(self, ch):
        
        if self.state == self.STATE_APPENDING:
            assert (self.cursor_pos_in_content() == len(self.content))
            if self.content_overflow_append():
                self.content += ch
                self.start_display_string = len(self.content) - (self.width - 1)
                self.display_string = self.content[len(self.content) - (self.width - 1): len(self.content)] + " "
                self.cpos_buffer = self.width - 1
            else:
                self.content += ch
                self.display_string = self.content + " "
                self.start_display_string = 0
                self.cpos_buffer = len(self.content) 
            # self.content_append_character(ch)
            # self.display_string = self.calc_append_display_string()
            # if len(self.content) <= (self.width - 2):
            #     self.content += ch
            #     self.display_string = self.content + " "
            #     self.start_display_string = 0
            #     self.cpos_buffer = len(self.content) 
            # else:
            #     self.content += ch
            #     self.start_display_string = len(self.content) - (self.width - 1)
            #     self.display_string = self.content[len(self.content) - (self.width - 1): len(self.content)] + " "
            #     self.cpos_buffer = self.width - 1
        else:
            pos = self.cursor_pos_in_content()
            self.content = self.content_insert_character(pos, ch)
            self.display_string = self.calc_display_string()

    # handle a backspace character. Delete the character on the left of the cursor
    # if there is one
    def handle_backspace(self):
        if self.state == self.STATE_APPENDING:
            if len(self.content) <= (self.width - 1):
                self.content = self.content[0: len(self.content) - 1]
                self.start_display_string = 0
                self.display_string = self.content + " "
                self.cpos_buffer = len(self.content) 
            else:
                self.content = self.content[0: len(self.content) - 1]
                self.start_display_string = len(self.content) - (self.width - 1)
                self.display_string = self.content[len(self.content) - (self.width - 1): len(self.content)] + " "
                self.cpos_buffer = self.width - 1
        else:
            if not self.cursor_at_content_start():
                del_pos = self.cursor_pos_in_content() - 1
                self.content = self.content_remove_character(del_pos)
                if self.start_display_string != 0:
                    self.start_display_string += -1
                    self.display_string = self.calc_display_string()
                else:
                    self.cpos_buffer += -1
                    self.display_string = self.calc_display_string()
            if len(self.content) == 0:
                self.state = self.STATE_APPENDING

    # handle delete  - in append mode do nothing
    # in edit mode delete the character under the cursor if there is one
    def handle_delete(self):
        if self.state == self.STATE_APPENDING:
            return
        if (self.cpos_buffer == self.width - 1) and (self.start_display_string + self.width) == len(self.content):
            pass
        else:
            if len(self.content) == 0:
                return
            pos = self.cursor_pos_in_content()
            self.content = self.content_remove_character(pos)
            self.display_string = self.calc_display_string()
            if len(self.content) == 0:
                self.state  = self.STATE_APPENDING
                self.display_string = self.content + self.EOSPAD

    
    # handle left arrow - 
    #   in append mode transitions to edit mode, move the cursor 1 character left and update state variable
    #   in edit mode move the cursor 1 spot left unless it is already at the start of the buffer. In which case
    #       move the window left one character and leave the cursor in the same position  
    def handle_left(self):
        if self.state == self.STATE_APPENDING:
            self.state = self.STATE_EDITING 
        if self.cpos_buffer > 0 and self.cpos_buffer <= self.width - 1:
            self.cpos_buffer -= 1
        elif self.cpos_buffer == 0:
            if self.start_display_string > 0:
                self.start_display_string -= 1
                end = self.start_display_string + self.width - 1
                self.display_string = self.content[self.start_display_string : end] + " "
            else:
                pass
        else:
            pass
    
    # handle right arrow key
    #   if in append mode do nothing
    #   if in edit mode
    #       if cursor is at the last content character
    #           move the buffer window one character right so the EOS character is in the last position
    #           put the cursor over the EOS character
    #           change mode to append 
    #       else
    #           if the cursor is in the last window position 
    #               move the buffer window 1 place left
    #               leave the cursor position in the window buffer unchanged
    #           else
    #               move the cursor position in the window 1 place right
    #               move the cursor position in the content string 1 place right  
    def handle_right(self):
        if self.cpos_buffer >= 0 and self.cpos_buffer < (self.width - 1):
            self.cpos_buffer += 1
        elif self.cpos_buffer == self.width - 1:
            # if self.start_display_string + self.width - 1 == len(self.content): # cannot move right any further
            #     pass
            if self.start_display_string < len(self.content) - 1 and (self.start_display_string + self.width - 1 != len(self.content)): # can move right
                self.start_display_string += 1 
                end = self.start_display_string + self.width - 1
                self.display_string = self.content[self.start_display_string : end] + " "
            else:
                pass
        else:
            pass
        if self.cursor_after_content_end():
            self.state = self.STATE_APPENDING

# 
# tests an input string to see if it represents an editing character
# 
def is_edit_character(ch):
    pass
def is_edit_back(ch):
    return (len(ch) == 1) and (ch[0] == 0x7f)

def is_edit_del(ch):
    return (ch == "KEY_DC")

def is_edit_move_back(ch):
    return (ch == "KEY_DC")

def is_edit_move_forward(ch):
    return (ch == "KEY_DC")


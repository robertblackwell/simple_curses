import sys
import unittest

import string_buffer

class TestStringBuffer(unittest.TestCase):

    def test_append_mode(self):
        sb = string_buffer.StringBuffer("", 5)
        self.assertEqual(sb.content, "")
        self.assertEqual(sb.display_string, "")
        self.assertEqual(sb.cpos_buffer, 0)

        sb.handle_character("a")
        self.assertEqual(sb.content, "a")
        self.assertEqual(sb.display_string, "a ")
        self.assertEqual(sb.cpos_buffer, 1)

        sb.handle_character("b")
        self.assertEqual(sb.content, "ab")
        self.assertEqual(sb.display_string, "ab"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 2)

        sb.handle_character("c")
        self.assertEqual(sb.content, "abc")
        self.assertEqual(sb.display_string, "abc"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 3)

        sb.handle_character("d")
        self.assertEqual(sb.content, "abcd")
        self.assertEqual(sb.display_string, "abcd"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)

        sb.handle_character("e")
        self.assertEqual(sb.content, "abcde")
        self.assertEqual(sb.display_string, "bcde"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)

        sb.handle_character("f")    
        self.assertEqual(sb.content, "abcdef")
        self.assertEqual(sb.display_string, "cdef"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)

        sb.handle_character("g")    
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "defg"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)

        sb.handle_character("h")    
        self.assertEqual(sb.content, "abcdefgh")
        self.assertEqual(sb.display_string, "efgh"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)

        sb.handle_backspace()    
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "defg"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)

        sb.handle_backspace()    
        self.assertEqual(sb.content, "abcdef")
        self.assertEqual(sb.display_string, "cdef"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)

        sb.handle_backspace()    
        self.assertEqual(sb.content, "abcde")
        self.assertEqual(sb.display_string, "bcde"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)

        sb.handle_backspace()    
        self.assertEqual(sb.content, "abcd")
        self.assertEqual(sb.display_string, "abcd"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)

        sb.handle_backspace()    
        self.assertEqual(sb.content, "abc")
        self.assertEqual(sb.display_string, "abc"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 3)

        sb.handle_backspace()    
        self.assertEqual(sb.content, "ab")
        self.assertEqual(sb.display_string, "ab"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 2)


    def test_left_arrow(self):
        sb = string_buffer.StringBuffer("abcdefg", 5)
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "defg" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

        sb.handle_left()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "defg" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 3)
        self.assertEqual(sb.state, sb.STATE_EDITING)
        
        sb.handle_left()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "defg" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 2)
        self.assertEqual(sb.state, sb.STATE_EDITING)
        
        sb.handle_left()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "defg" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 1)
        self.assertEqual(sb.state, sb.STATE_EDITING)
        
        sb.handle_left()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "defg" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)
        
        sb.handle_left()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "cdef" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)
        
        sb.handle_left()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "bcde" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)
        
        sb.handle_left()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "abcd" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)
        
        sb.handle_left()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "abcd" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)

    def test_right_arrow(self):
        sb = string_buffer.StringBuffer("abcdefg", 5)
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "defg" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)

        sb.handle_left()
        sb.handle_left()
        sb.handle_left()
        sb.handle_left()
        sb.handle_left()
        sb.handle_left()
        sb.handle_left()
        sb.handle_left()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "abcd" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_right()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "abcd" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 1)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_right()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "abcd" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 2)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_right()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "abcd" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 3)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_right()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "abcd" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_right()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "bcde" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_right()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "cdef" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_right()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "defg" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

        sb.handle_right()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "defg" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

        sb.handle_right()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "defg" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

        sb.handle_right()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "defg" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

    def test_edit_backspace(self):
        sb = string_buffer.StringBuffer("abcdefg", 5)
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "defg" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)

        sb.handle_left()
        sb.handle_left()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "defg" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 2)
        self.assertEqual(sb.state, sb.STATE_EDITING)


        sb.handle_backspace()
        self.assertEqual(sb.content, "abcdfg")
        self.assertEqual(sb.display_string, "cdfg")
        self.assertEqual(sb.cpos_buffer, 2)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_backspace()
        self.assertEqual(sb.content, "abcfg")
        self.assertEqual(sb.display_string, "bcfg")
        self.assertEqual(sb.cpos_buffer, 2)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_backspace()
        self.assertEqual(sb.content, "abfg")
        self.assertEqual(sb.display_string, "abfg")
        self.assertEqual(sb.cpos_buffer, 2)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_backspace()
        self.assertEqual(sb.content, "afg")
        self.assertEqual(sb.display_string, "afg")
        self.assertEqual(sb.cpos_buffer, 1)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_backspace()
        self.assertEqual(sb.content, "fg")
        self.assertEqual(sb.display_string, "fg")
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_backspace()
        self.assertEqual(sb.content, "fg")
        self.assertEqual(sb.display_string, "fg")
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)

    def test_edit_delete(self):
        sb = string_buffer.StringBuffer("abcdefg", 5)
        sb.handle_left()
        sb.handle_left()
        sb.handle_left()
        sb.handle_left()
        sb.handle_left()
        sb.handle_left()
        sb.handle_left()
        sb.handle_left()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "abcd" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_delete()
        self.assertEqual(sb.content, "bcdefg")
        self.assertEqual(sb.display_string, "bcde")
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_delete()
        self.assertEqual(sb.content, "cdefg")
        self.assertEqual(sb.display_string, "cdef")
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_delete()
        self.assertEqual(sb.content, "defg")
        self.assertEqual(sb.display_string, "defg")
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_delete()
        self.assertEqual(sb.content, "efg")
        self.assertEqual(sb.display_string, "efg")
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_delete()
        self.assertEqual(sb.content, "fg")
        self.assertEqual(sb.display_string, "fg")
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_delete()
        self.assertEqual(sb.content, "g")
        self.assertEqual(sb.display_string, "g")
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_delete()
        self.assertEqual(sb.content, "")
        self.assertEqual(sb.display_string, "" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

    def test_edit_insert(self):
        sb = string_buffer.StringBuffer("abcdefg", 5)
        sb.handle_left()
        sb.handle_left()
        sb.handle_left()
        self.assertEqual(sb.display_string, "defg" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 1)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_character("X")
        self.assertEqual(sb.content, "abcdXefg")
        self.assertEqual(sb.display_string, "dXef")
        self.assertEqual(sb.cpos_buffer, 1)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_character("Y")
        self.assertEqual(sb.content, "abcdYXefg")
        self.assertEqual(sb.display_string, "dYXe")
        self.assertEqual(sb.cpos_buffer, 1)
        self.assertEqual(sb.state, sb.STATE_EDITING)

    def test_edit_insert_at_beginning(self):
        sb = string_buffer.StringBuffer("abcdefg", 5)
        sb.handle_left()
        sb.handle_left()
        sb.handle_left()
        sb.handle_left()
        sb.handle_left()
        sb.handle_left()
        sb.handle_left()
        sb.handle_left()
        self.assertEqual(sb.display_string, "abcd" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_character("X")
        self.assertEqual(sb.content, "Xabcdefg")
        self.assertEqual(sb.display_string, "Xabc")
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_character("Y")
        self.assertEqual(sb.content, "YXabcdefg")
        self.assertEqual(sb.display_string, "YXab")
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)


if __name__ == '__main__':
    unittest.main()
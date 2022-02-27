import sys
import unittest

import string_buffer

class TestStringBufferAppend(unittest.TestCase):

    def test_append_mode(self):
        sb = string_buffer.StringBuffer("", 5)
        self.assertEqual(sb.content, "")
        self.assertEqual(sb.dstring, "")
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

        sb.handle_character("a")
        self.assertEqual(sb.content, "a")
        self.assertEqual(sb.dstring, "a ")
        self.assertEqual(sb.cpos_buffer, 1)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

        sb.handle_character("b")
        self.assertEqual(sb.content, "ab")
        self.assertEqual(sb.dstring, "ab"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 2)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

        sb.handle_character("c")
        self.assertEqual(sb.content, "abc")
        self.assertEqual(sb.dstring, "abc"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 3)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

        sb.handle_character("d")
        self.assertEqual(sb.content, "abcd")
        self.assertEqual(sb.dstring, "abcd"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

        sb.handle_character("e")
        self.assertEqual(sb.content, "abcde")
        self.assertEqual(sb.dstring, "bcde"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

        sb.handle_character("f")    
        self.assertEqual(sb.content, "abcdef")
        self.assertEqual(sb.dstring, "cdef"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

        sb.handle_character("g")    
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.dstring, "defg"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

        sb.handle_character("h")    
        self.assertEqual(sb.content, "abcdefgh")
        self.assertEqual(sb.dstring, "efgh"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

        sb.handle_backspace()    
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.dstring, "defg"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

        sb.handle_backspace()    
        self.assertEqual(sb.content, "abcdef")
        self.assertEqual(sb.dstring, "cdef"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

        sb.handle_backspace()    
        self.assertEqual(sb.content, "abcde")
        self.assertEqual(sb.dstring, "bcde"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

        sb.handle_backspace()    
        self.assertEqual(sb.content, "abcd")
        self.assertEqual(sb.dstring, "abcd"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

        sb.handle_backspace()    
        self.assertEqual(sb.content, "abc")
        self.assertEqual(sb.dstring, "abc"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 3)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

        sb.handle_backspace()    
        self.assertEqual(sb.content, "ab")
        self.assertEqual(sb.dstring, "ab"+sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 2)
        self.assertEqual(sb.state, sb.STATE_APPENDING)


if __name__ == '__main__':
    unittest.main()
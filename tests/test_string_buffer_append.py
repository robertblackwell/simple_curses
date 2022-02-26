import sys
import unittest

print(sys.path)

import string_buffer

class TestStringBufferAppend(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
import sys
import unittest

import string_buffer

class TestStringBuffer(unittest.TestCase):


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


if __name__ == '__main__':
    unittest.main()
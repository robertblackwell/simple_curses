import sys
import unittest

import string_buffer

class TestStringBufferRight(unittest.TestCase):


    def test_right_arrow_01(self):
        sb = string_buffer.StringBuffer("abc", 5)
        self.assertEqual(sb.content, "abc")
        self.assertEqual(sb.display_string, "abc" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 3)

        sb.handle_left()
        sb.handle_left()
        sb.handle_left()
        self.assertEqual(sb.content, "abc")
        self.assertEqual(sb.display_string, "abc" + sb.EOSPAD)
        self.assertEqual(sb.dstring, "abc")
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_right()
        self.assertEqual(sb.content, "abc")
        self.assertEqual(sb.display_string, "abc" + sb.EOSPAD)
        self.assertEqual(sb.dstring, "abc")
        self.assertEqual(sb.cpos_buffer, 1)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_right()
        self.assertEqual(sb.content, "abc")
        self.assertEqual(sb.display_string, "abc" + sb.EOSPAD)
        self.assertEqual(sb.dstring, "abc")
        self.assertEqual(sb.cpos_buffer, 2)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_right()
        self.assertEqual(sb.content, "abc")
        self.assertEqual(sb.display_string, "abc" + sb.EOSPAD)
        self.assertEqual(sb.dstring, "abc" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 3)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

        sb.handle_right()
        self.assertEqual(sb.content, "abc")
        self.assertEqual(sb.display_string, "abc" + sb.EOSPAD)
        self.assertEqual(sb.dstring, "abc" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 3)
        self.assertEqual(sb.state, sb.STATE_APPENDING)


    def test_right_arrow_02(self):
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
        self.assertEqual(sb.dstring, "abcde")
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_right()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "abcd" + sb.EOSPAD)
        self.assertEqual(sb.dstring, "abcde")
        self.assertEqual(sb.cpos_buffer, 1)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_right()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "abcd" + sb.EOSPAD)
        self.assertEqual(sb.dstring, "abcde")
        self.assertEqual(sb.cpos_buffer, 2)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_right()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "abcd" + sb.EOSPAD)
        self.assertEqual(sb.dstring, "abcde")
        self.assertEqual(sb.cpos_buffer, 3)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_right()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "abcd" + sb.EOSPAD)
        self.assertEqual(sb.dstring, "abcde")
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_right()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "bcde" + sb.EOSPAD)
        self.assertEqual(sb.dstring, "bcdef")
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_right()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "cdef" + sb.EOSPAD)
        self.assertEqual(sb.dstring, "cdefg")
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_right()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "defg" + sb.EOSPAD)
        self.assertEqual(sb.dstring, "defg" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

        sb.handle_right()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "defg" + sb.EOSPAD)
        self.assertEqual(sb.dstring, "defg" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

        sb.handle_right()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "defg" + sb.EOSPAD)
        self.assertEqual(sb.dstring, "defg" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

        sb.handle_right()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "defg" + sb.EOSPAD)
        self.assertEqual(sb.dstring, "defg" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_APPENDING)


if __name__ == '__main__':
    unittest.main()
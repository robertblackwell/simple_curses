import sys
import unittest

import string_buffer

class TestStringBufferBackspace(unittest.TestCase):

    def test_edit_backspace(self):
        sb = string_buffer.StringBuffer("abcdefg", 5)
        self.assertEqual(sb.content, "abcdefg")
        # self.assertEqual(sb.display_string, "defg" + sb.EOSPAD)
        self.assertEqual(sb.dstring, "defg" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)
        self.assertEqual(sb.state, sb.STATE_APPENDING)

        sb.handle_left()
        sb.handle_left()
        self.assertEqual(sb.content, "abcdefg")
        # self.assertEqual(sb.display_string, "defg" + sb.EOSPAD)
        self.assertEqual(sb.dstring, "defg")
        self.assertEqual(sb.cpos_buffer, 2)
        self.assertEqual(sb.state, sb.STATE_EDITING)


        sb.handle_backspace()
        self.assertEqual(sb.content, "abcdfg")
        # self.assertEqual(sb.display_string, "cdfg")
        self.assertEqual(sb.dstring, "cdfg")
        self.assertEqual(sb.cpos_buffer, 2)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_backspace()
        self.assertEqual(sb.content, "abcfg")
        # self.assertEqual(sb.display_string, "bcfg")
        self.assertEqual(sb.dstring, "bcfg")
        self.assertEqual(sb.cpos_buffer, 2)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_backspace()
        self.assertEqual(sb.content, "abfg")
        # self.assertEqual(sb.display_string, "abfg")
        self.assertEqual(sb.dstring, "abfg")
        self.assertEqual(sb.cpos_buffer, 2)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_backspace()
        self.assertEqual(sb.content, "afg")
        # self.assertEqual(sb.display_string, "afg")
        self.assertEqual(sb.dstring, "afg")
        self.assertEqual(sb.cpos_buffer, 1)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_backspace()
        self.assertEqual(sb.content, "fg")
        # self.assertEqual(sb.display_string, "fg")
        self.assertEqual(sb.dstring, "fg")
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_backspace()
        self.assertEqual(sb.content, "fg")
        # self.assertEqual(sb.display_string, "fg")
        self.assertEqual(sb.dstring, "fg")
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)


if __name__ == '__main__':
    unittest.main()
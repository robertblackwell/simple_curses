import sys
import unittest

import string_buffer


class TestStringBufferDelete(unittest.TestCase):

    def test_edit_delete(self):
        sb = string_buffer.StringBuffer("abcdefg", 5)
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "defg" + sb.EOSPAD)
        self.assertEqual(sb.cpos_buffer, 4)
        sb.handle_left()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "defg")
        self.assertEqual(sb.cpos_buffer, 3)
        sb.handle_left()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "defg")
        self.assertEqual(sb.cpos_buffer, 2)
        sb.handle_left()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "defg")
        self.assertEqual(sb.cpos_buffer, 1)
        sb.handle_left()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "defg")
        self.assertEqual(sb.cpos_buffer, 0)
        sb.handle_left()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "cdefg")
        self.assertEqual(sb.cpos_buffer, 0)
        sb.handle_left()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "bcdef")
        self.assertEqual(sb.cpos_buffer, 0)
        sb.handle_left()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "abcde")
        self.assertEqual(sb.cpos_buffer, 0)
        sb.handle_left()
        self.assertEqual(sb.content, "abcdefg")
        self.assertEqual(sb.display_string, "abcde")
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_delete()
        self.assertEqual(sb.content, "bcdefg")
        self.assertEqual(sb.display_string, "bcdef")
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_delete()
        self.assertEqual(sb.content, "cdefg")
        self.assertEqual(sb.display_string, "cdefg")
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


if __name__ == '__main__':
    unittest.main()

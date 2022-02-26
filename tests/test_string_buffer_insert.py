import sys
import os
import unittest

print(sys.path)
test_dir = os.path.dirname(__file__)
project_dir = os.path.dirname(os.path.dirname(__file__))
src_dir = os.path.join(project_dir, "simple_curses")
project_dir = os.path.abspath("../")
if not project_dir in sys.path:
    print("Adding to sys.path")
    sys.path.append(project_dir)
    sys.path.append(src_dir)

import string_buffer

class TestStringBufferInsert(unittest.TestCase):

    def test_edit_insert(self):
        sb = string_buffer.StringBuffer("abcdefg", 5)
        sb.handle_left()
        sb.handle_left()
        sb.handle_left()
        self.assertEqual(sb.display_string, "defg" + sb.EOSPAD)
        self.assertEqual(sb.dstring, "defg")
        self.assertEqual(sb.cpos_buffer, 1)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_character("X")
        self.assertEqual(sb.content, "abcdXefg")
        self.assertEqual(sb.display_string, "dXef")
        self.assertEqual(sb.dstring, "dXefg")
        self.assertEqual(sb.cpos_buffer, 1)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_character("Y")
        self.assertEqual(sb.content, "abcdYXefg")
        self.assertEqual(sb.display_string, "dYXe")
        self.assertEqual(sb.dstring, "dYXef")
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
        self.assertEqual(sb.dstring, "abcde")
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_character("X")
        self.assertEqual(sb.content, "Xabcdefg")
        self.assertEqual(sb.display_string, "Xabc")
        self.assertEqual(sb.dstring, "Xabcd")
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_character("Y")
        self.assertEqual(sb.content, "YXabcdefg")
        self.assertEqual(sb.display_string, "YXab")
        self.assertEqual(sb.dstring, "YXabc")
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)


if __name__ == '__main__':
    unittest.main()
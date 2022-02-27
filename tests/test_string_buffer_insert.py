import sys
import os
import unittest

# print(sys.path)
# test_dir = os.path.dirname(__file__)
# project_dir = os.path.dirname(os.path.dirname(__file__))
# src_dir = os.path.join(project_dir, "simple_curses")
# project_dir = os.path.abspath("../")
# if not project_dir in sys.path:
#     print("Adding to sys.path")
#     sys.path.append(project_dir)
#     sys.path.append(src_dir)

import string_buffer

class TestStringBufferInsert(unittest.TestCase):

    def test_edit_insert(self):
        sb = string_buffer.StringBuffer("abcdefg", 5)
        sb.handle_left()
        sb.handle_left()
        sb.handle_left()
        self.assertEqual(sb.display_string, "defg")
        self.assertEqual(sb.cpos_buffer, 1)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_character("X")
        self.assertEqual(sb.content, "abcdXefg")
        self.assertEqual(sb.display_string, "dXefg")
        self.assertEqual(sb.cpos_buffer, 2)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_character("Y")
        self.assertEqual(sb.content, "abcdXYefg")
        self.assertEqual(sb.display_string, "dXYef")
        self.assertEqual(sb.cpos_buffer, 3)
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
        self.assertEqual(sb.display_string, "abcde")
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_character("X")
        self.assertEqual(sb.content, "Xabcdefg")
        self.assertEqual(sb.display_string, "Xabcd")
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)

        sb.handle_character("Y")
        self.assertEqual(sb.content, "YXabcdefg")
        self.assertEqual(sb.display_string, "YXabc")
        self.assertEqual(sb.cpos_buffer, 0)
        self.assertEqual(sb.state, sb.STATE_EDITING)


if __name__ == '__main__':
    unittest.main()
import unittest
import ipaddress
import time

from partitian import Partitian


class TestValidator(unittest.TestCase):

    def test_partitian(self):
        part = Partitian(178, 3)
        self.assertNotEqual(part.groups, None)


if __name__ == '__main__':
    unittest.main()

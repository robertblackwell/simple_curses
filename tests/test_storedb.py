import sys
import unittest

from store_db import *


class TestStringBufferAppend(unittest.TestCase):

    def test_get_store(self):
        store = StoreDatabase.get_store("S87603")
        print("hello")


if __name__ == '__main__':
    unittest.main()

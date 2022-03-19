import unittest
import ipaddress
import time

import validator


class TestValidator(unittest.TestCase):

    def test_integer(self):
        val = validator.Integer()
        self.assertEqual(val.validate("12345"), 12345)
        self.assertEqual(val.validate("12s"), None)

    def test_float(self):
        val = validator.Float()
        self.assertEqual(val.validate("12345"), 12345.0)
        self.assertEqual(val.validate("12345.987"), 12345.987)
        self.assertEqual(val.validate("123x45.987"), None)

    def test_ipaddress(self):
        val = validator.IPAddress()
        self.assertIsInstance(val.validate("192.168.1.0"), ipaddress.IPv4Address)
        self.assertIsInstance(val.validate("2001:0db8:85a3:0000:0000:8a2e:0370:7334"), ipaddress.IPv6Address)
        self.assertEqual(val.validate("2001:0db8:8X5a3:0000:0000:8a2e:0370:7334"), None)

    def test_ipnetwork(self):
        val = validator.IPNetwork()
        self.assertIsInstance(val.validate("192.168.1.0/255.255.255.0"), ipaddress.IPv4Network)
        self.assertIsInstance(val.validate("192.168.1.0/24"), ipaddress.IPv4Network)
        self.assertIsInstance(val.validate("2001:db00::0/24"), ipaddress.IPv6Network)
        self.assertEqual(val.validate("2001:db00::0/ffff:ff00::"), None)

    def test_tomeofday24(self):
        t1 = time.strptime("01:23 PM", "%H:%M %p")
        t2 = time.strptime("01:23 AM", "%H:%M %p")
        val = validator.TimeOfDay24()
        tstr = "1:24"
        expected = "01:24"
        t = val.validate(tstr)
        self.assertIsInstance(t, time.struct_time)
        z = time.strftime("%H:%M %p", t)
        self.assertEqual(time.strftime("%H:%M", t), expected)

        tstr = "01:24"
        expected = tstr
        t = val.validate(tstr)
        self.assertIsInstance(t, time.struct_time)
        self.assertEqual(time.strftime("%H:%M", t),tstr)
        
        tstr = "28:24"
        t = val.validate(tstr)
        self.assertEqual(t, None)
        
    def test_tomeofday12(self):
        val = validator.TimeOfDay12()
        tstr = "1:24 AM"
        expected = "01:24 AM"
        t = val.validate(tstr)
        self.assertIsInstance(t, time.struct_time)
        z = time.strftime("%H:%M %p", t)
        self.assertEqual(time.strftime("%H:%M %p", t), expected)

        tstr = "01:24 PM"
        expected = "13:24"
        t = val.validate(tstr)
        z = time.strftime("%H:%M %p", t)
        self.assertIsInstance(t, time.struct_time)
        self.assertEqual(time.strftime("%H:%M", t),expected)
        
        tstr = "13:24 AM"
        t = val.validate(tstr)
        self.assertEqual(t, None)
        

class MyClass:
    def __init__(self):
        self.value = "thisisthevalue of a property"

    def cmethod():
        print("cmethod")


class TestClassMethods(unittest.TestCase):

    def test_ClassMethods(self):
        MyClass.cmethod()


if __name__ == '__main__':
    unittest.main()

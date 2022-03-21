import unittest
import ipaddress
import time
import os
import sys

print("sys.path {}".format(sys.path))
test_dir = os.path.dirname(__file__)
project_dir = os.path.dirname(os.path.dirname(__file__))
src_dir = os.path.join(project_dir, "simple_curses")
project_dir = os.path.abspath("../")

print("project_dir {}".format(project_dir))
print("test_dir {}".format(test_dir))
print("src dir {}".format(src_dir))

if not project_dir in sys.path:
    print("Adding to sys.path")
    sys.path.append(project_dir)
    sys.path.append(src_dir)

print("sys.path {}".format(sys.path))


from layout import ColumnLayout
from text_widget import IPAddressWidget, IPNetworkWidget, IntegerWidget, FloatWidget, TimeOfDayWidget, TextWidget
from toggle_widget import ToggleWidget
from multi_line_widget import MultiLineWidget

data = "some dta"
view_widgets_02 = [

        IPNetworkWidget(2, 2, "ipnet_11", "IPNetwork         ", 20, "", data),
        IntegerWidget(4, 2, "int_val_11", "Integer           ", 20, "", data),
        FloatWidget(6, 2, "float_val_11", "Float             ", 20, "", data),
        IPAddressWidget(8, 2, "ipaddr_11", "IPAddr            ", 20, "", data),
        TimeOfDayWidget(10, 2, "tod_11", "Time Of Day (24h) ", 20, "", data),
        TextWidget(12, 2, "text_11", "Text              ", 20, "", data),
        ToggleWidget(14, 2, "toggle_11", "Toggle            ", 3, "", data, ['ENABLED', "DISABLED"], "DISABLED"),
        IPNetworkWidget(2, 2, "ipnet_22", "IPNetwork         ", 20, "", data),
        IntegerWidget(4, 2, "int_val_22", "Integer           ", 20, "", data),
        FloatWidget(6, 2, "float_val_22", "Float             ", 20, "", data),
        MultiLineWidget(key="sc_11", label="IPv4 and IPv6 Networks in CIDR Format", content_width=50, content_height=10, attributes="", data=data),
        # DropdownWidget (16, 90, "dd_01", "Selection",   55, 10, "", data, ["one","two","three","four"], "three"),
    ]

view_widgets_01 = [

        IPNetworkWidget(2, 2, "ipnet_01", "IPNetwork         ", 20, "", data),
        IntegerWidget(4, 2, "int_val_01", "Integer           ", 20, "", data),
        FloatWidget(6, 2, "float_val_01", "Float             ", 20, "", data),
        IPAddressWidget(8, 2, "ipaddr_01", "IPAddr            ", 20, "", data),
        TimeOfDayWidget(10, 2, "tod_01", "Time Of Day (24h) ", 20, "", data),
        TextWidget(12, 2, "text_01", "Text              ", 20, "", data),
        ToggleWidget(14, 2, "toggle_01", "Toggle            ", 3, "", data, ['ENABLED', "DISABLED"], "DISABLED"),
        IPNetworkWidget(2, 2, "ipnet_02", "IPNetwork         ", 20, "", data),
        IntegerWidget(4, 2, "int_val_02", "Integer           ", 20, "", data),
        FloatWidget(6, 2, "float_val_02", "Float             ", 20, "", data),
        IPAddressWidget(8, 2, "ipaddr_02", "IPAddr            ", 20, "", data),
        TimeOfDayWidget(10, 2, "tod_02", "Time Of Day (24h) ", 20, "", data),
        TextWidget(12, 2, "text_02", "Text              ", 20, "", data),
        ToggleWidget(14, 2, "toggle_02", "Toggle            ", 3, "", data, ['ENABLED', "DISABLED"], "DISABLED"),
        IPNetworkWidget(2, 2, "ipnet_03", "IPNetwork         ", 20, "", data),
        IntegerWidget(4, 2, "int_val_03", "Integer           ", 20, "", data),
        FloatWidget(6, 2, "float_val_03", "Float             ", 20, "", data),
        IPAddressWidget(8, 2, "ipaddr_03", "IPAddr            ", 20, "", data),
        TimeOfDayWidget(10, 2, "tod_03", "Time Of Day (24h) ", 20, "", data),
        TextWidget(12, 2, "text_03", "Text              ", 20, "", data),
        ToggleWidget(14, 2, "toggle_03", "Toggle            ", 3, "", data, ['ENABLED', "DISABLED"], "DISABLED"),
        IPNetworkWidget(2, 2, "ipnet_04", "IPNetwork         ", 20, "", data),
        IntegerWidget(4, 2, "int_val_04", "Integer           ", 20, "", data),
        FloatWidget(6, 2, "float_val_04", "Float             ", 20, "", data),
        IPAddressWidget(8, 2, "ipaddr_04", "IPAddr            ", 20, "", data),
        TimeOfDayWidget(10, 2, "tod_04", "Time Of Day (24h) ", 20, "", data),
        TextWidget(12, 2, "text_04", "Text              ", 20, "", data),
        ToggleWidget(14, 2, "toggle_04", "Toggle            ", 3, "", data, ['ENABLED', "DISABLED"], "DISABLED"),
        MultiLineWidget(key="sc_01", label="IPv4 and IPv6 Networks in CIDR Format", content_width=50, content_height=10, attributes="", data=data),
        # DropdownWidget (16, 90, "dd_01", "Selection",   55, 10, "", data, ["one","two","three","four"], "three"),
    ]

def max_width(widgets):
    m = 0
    for w in widgets:
        m = w.get_width() if m < w.get_width() else m
    return m

class TestColumnLayout(unittest.TestCase):

    def test_column_layout_01(self):
        m = max_width(view_widgets_02)
        y_max = 28
        x_max = 178
        cl = ColumnLayout(y_max, m)
        cl.add_widgets(view_widgets_02)
        self.assertGreaterEqual(y_max, cl.get_ymax())
        self.assertEqual(cl.column_count(), 2)
        count = 0
        for ci in range(0, cl.column_count()):
            for wi in range(0, cl.widget_count(ci)):
                count += 1
                wl = cl.get_widget_layout(ci, wi)
                print("count: {} ci: {} wi: {} klass: {} wl.y_begin: {} wl.ymax: {} wl.y_begin + wl.ymax: {} wl.x_begin {} wl.xmax {} wl.x_begin + wl.xmax: {}"
                    .format(count, ci, wi, wl.widget.__class__, wl.y_begin, wl.ymax, wl.y_begin+wl.ymax, wl.x_begin, wl.xmax, wl.x_begin+wl.xmax))
                self.assertTrue(0 <= wl.y_begin < y_max)
                self.assertTrue(wl.y_begin + wl.ymax <= y_max)
                self.assertTrue(0 <= wl.x_begin < x_max)
                self.assertTrue(wl.x_begin + wl.xmax <= x_max)
        self.assertEqual(count, len(view_widgets_02))
        print("hello")

    def test_column_layout_11(self):
        m = max_width(view_widgets_01)
        y_max = 29
        x_max = 178
        cl = ColumnLayout(y_max, m)
        cl.add_widgets(view_widgets_01)
        self.assertGreaterEqual(y_max, cl.get_ymax())
        self.assertEqual(cl.column_count(), 3)
        count = 0
        for ci in range(0, cl.column_count()):
            for wi in range(0, cl.widget_count(ci)):
                count += 1
                wl = cl.get_widget_layout(ci, wi)
                print("count: {} ci: {} wi: {} klass: {} wl.y_begin: {} wl.ymax: {} wl.y_begin + wl.ymax: {} wl.x_begin {} wl.xmax {} wl.x_begin + wl.xmax: {}"
                    .format(count, ci, wi, wl.widget.__class__, wl.y_begin, wl.ymax, wl.y_begin+wl.ymax, wl.x_begin, wl.xmax, wl.x_begin+wl.xmax))
                self.assertTrue(0 <= wl.y_begin < y_max)
                self.assertTrue(wl.y_begin + wl.ymax <= y_max)
                self.assertTrue(0 <= wl.x_begin < x_max)
                self.assertTrue(wl.x_begin + wl.xmax <= x_max)
        self.assertEqual(count, len(view_widgets_01))
        print("hello")



    # def test_column_layout_02(self):
    #     m = max_width(view_widgets_02)
    #     cl = ColumnLayout(12, m)
    #     cl.add_widgets(view_widgets_02[0:9])
    #     mh = cl.widget_allocation.get_ymax()
    #     self.assertGreaterEqual(12, mh)
    #     self.assertEqual(cl.column_count(), 3)


if __name__ == '__main__':
    unittest.main()

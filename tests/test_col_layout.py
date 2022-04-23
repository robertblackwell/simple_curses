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


from layout import ColumnLayout, allocate_multiple_columns
from text_widget import IPAddressWidget, IPNetworkWidget, IntegerWidget, FloatWidget, TimeOfDayWidget, TextWidget
from toggle_widget import ToggleWidget
from multi_line_widget import MultiLineWidget

data = "some dta"
app = {}

small_example = [  
    [
        #  width 34
        IPNetworkWidget(app, "ipnet_11", "123456789012345678", 12, data),
        #  width 35
        IntegerWidget(app, "int_val_11", "Integer           ", 13, data),
        #  width 43
        FloatWidget(app, "float_val_11", "Float             ", 21, data),
    ],
    [ 
        # width 45
        IPNetworkWidget(app, "ipnet_11", "IPNetwork         ", 23, data),
        #width 34
        IntegerWidget(app, "int_val_11", "Integer           ", 12, data),
    ]
]

view_widgets_02 = [

        IPNetworkWidget(app, "ipnet_11", "IPNetwork         ", 20, data),
        IntegerWidget(app, "int_val_11", "Integer           ", 20, data),
        FloatWidget(app, "float_val_11", "Float             ", 20, data),
        IPAddressWidget(app, "ipaddr_11", "IPAddr            ", 20, data),
        TimeOfDayWidget(app, "tod_11", "Time Of Day (24h) ", 20, data),
        TextWidget(app, "text_11", "Text              ", 20, data),
        ToggleWidget(app, "toggle_11", "Toggle            ", 3, data, ['ENABLED']),
        IPNetworkWidget(app, "ipnet_22", "IPNetwork         ", 20, data),
        IntegerWidget(app, "int_val_22", "Integer           ", 20, data),
        FloatWidget(app, "float_val_22", "Float             ", 20, data),
        MultiLineWidget(app, key="sc_11", label="IPv4 and IPv6 Networks in CIDR Format", content_width=50, content_height=10, data=data),
        # DropdownWidget (16, 90, "dd_01", "Selection",   55, 10, "", data, ["one","two","three","four"], "three"),
    ]

view_widgets_01 = [

        IPNetworkWidget(app, "ipnet_01", "IPNetwork         ", 20, data),
        IntegerWidget(app, "int_val_01", "Integer           ", 20, data),
        FloatWidget(app, "float_val_01", "Float             ", 20, data),
        IPAddressWidget(app, "ipaddr_01", "IPAddr            ", 20, data),
        TimeOfDayWidget(app, "tod_01", "Time Of Day (24h) ", 20, data),
        TextWidget(app, "text_01", "Text              ", 20, data),
        ToggleWidget(app, "toggle_01", "Toggle            ", 3, data, ['ENABLED', "DISABLED"]),
        IPNetworkWidget(app, "ipnet_02", "IPNetwork         ", 20, data),
        IntegerWidget(app, "int_val_02", "Integer           ", 20, data),
        FloatWidget(app, "float_val_02", "Float             ", 20, data),
        IPAddressWidget(app, "ipaddr_02", "IPAddr            ", 20, data),
        TimeOfDayWidget(app, "tod_02", "Time Of Day (24h) ", 20, data),
        TextWidget(app, "text_02", "Text              ", 20, data),
        ToggleWidget(app, "toggle_02", "Toggle            ", 3, data, ['ENABLED', "DISABLED"]),
        IPNetworkWidget(app, "ipnet_03", "IPNetwork         ", 20, data),
        IntegerWidget(app, "int_val_03", "Integer           ", 20, data),
        FloatWidget(app, "float_val_03", "Float             ", 20, data),
        IPAddressWidget(app, "ipaddr_03", "IPAddr            ", 20, data),
        TimeOfDayWidget(app, "tod_03", "Time Of Day (24h) ", 20, data),
        TextWidget(app, "text_03", "Text              ", 20, data),
        ToggleWidget(app, "toggle_03", "Toggle            ", 3, data, ['ENABLED', "DISABLED"]),
        IPNetworkWidget(app, "ipnet_04", "IPNetwork         ", 20, data),
        IntegerWidget(app, "int_val_04", "Integer           ", 20, data),
        FloatWidget(app, "float_val_04", "Float             ", 20, data),
        IPAddressWidget(app, "ipaddr_04", "IPAddr            ", 20, data),
        TimeOfDayWidget(app, "tod_04", "Time Of Day (24h) ", 20, data),
        TextWidget(app, "text_04", "Text              ", 20, data),
        ToggleWidget(app, "toggle_04", "Toggle            ", 3, data, ['ENABLED', "DISABLED"]),
        MultiLineWidget(app, key="sc_01", label="IPv4 and IPv6 Networks in CIDR Format", content_width=50, content_height=10, data=data),
        # DropdownWidget (16, 90, "dd_01", "Selection",   55, 10, "", data, ["one","two","three","four"], "three"),
    ]

def max_width(widgets):
    m = 0
    for w in widgets:
        m = w.get_width() if m < w.get_width() else m
    return m

class testA(unittest.TestCase):
    def test_2_cols(self):
        widgets = small_example
        w00 = small_example[0][0].get_width()
        w01 = small_example[0][1].get_width()
        w02 = small_example[0][2].get_width()
        h00 = small_example[0][0].get_height()
        h01 = small_example[0][1].get_height()
        h02 = small_example[0][2].get_height()
        h0f = 1 + h00 + h01 + h02 + 1

        w10 = small_example[1][0].get_width()
        w11 = small_example[1][1].get_width()
        h10 = small_example[1][0].get_height()
        h11 = small_example[1][1].get_height()
        h1f = 1 + h10 + h11 + 1

        wa = allocate_multiple_columns(widgets)
        h = wa.get_height()
        w = wa.get_width()
        self.assertEqual(h, 5)
        self.assertEqual(w, 45+47)
        self.assertEquals(wa.widget_columns[0].widget_layouts[0].y_begin, 1)
        self.assertEquals(wa.widget_columns[0].widget_layouts[1].y_begin, 2)
        self.assertEquals(wa.widget_columns[0].widget_layouts[2].y_begin, 3)

        self.assertEquals(wa.widget_columns[0].widget_layouts[0].x_begin, 1)
        self.assertEquals(wa.widget_columns[0].widget_layouts[1].x_begin, 1)
        self.assertEquals(wa.widget_columns[0].widget_layouts[2].x_begin, 1)

        self.assertEquals(wa.widget_columns[1].widget_layouts[0].y_begin, 1)
        self.assertEquals(wa.widget_columns[1].widget_layouts[1].y_begin, 2)

        self.assertEquals(wa.widget_columns[1].widget_layouts[0].x_begin, 46)
        self.assertEquals(wa.widget_columns[1].widget_layouts[1].x_begin, 46)
        print("hello")

class TestColumnLayout(unittest.TestCase):

    def test_column_layout_01(self):
        return
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
        return
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

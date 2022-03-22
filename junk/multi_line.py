import sys
import os
import curses

requiredHeight = 30
requiredWidth = 180

# print(sys.path)
test_dir = os.path.dirname(__file__)
project_dir = os.path.dirname(os.path.dirname(__file__))
src_dir = os.path.join(project_dir, "simple_curses")
project_dir = os.path.abspath("../")
if not project_dir in sys.path:
    # print("Adding to sys.path")
    sys.path.append(project_dir)
    sys.path.append(src_dir)

from simple_curses.text_widget import TextWidget, IntegerWidget, FloatWidget, IPAddressWidget, IPNetworkWidget, \
    TimeOfDayWidget
from simple_curses.menu import MenuItem
from simple_curses.multi_line_widget import MultiLineWidget
from dropdown_widget import DropdownWidget
from simple_curses.toggle_widget import ToggleWidget
from simple_curses.form import Form, ViewBody


def testScreenSize(stdscr):
    h, w = stdscr.getmaxyx()
    if h < requiredHeight or w < requiredWidth:
        raise Exception(
            "SCreen is too small must be at least {} high and {} wide currently is high: {} wide: {}".format(
                requiredHeight, requiredWidth, h, w))


def menu_action_0(form, context):
    form.msg_info("menu action 0")


def menu_action_1(form, context):
    v = form.get_values()
    s = ""
    if v is not None:
        for k in v.keys():
            s += "v[{}] = {}, ".format(k, v[k])

    form.msg_info("menu action 1 {}".format(v))
    # run a command with elements of v as arguments


def menuAction2(form, context):
    form.msg_info("menu action 2")


def menuAction3(form, context):
    form.msg_info("menu action 3")


def main(stdscr):
    data = "dummy context"
    testScreenSize(stdscr)
    curses.curs_set(2)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    left_widgets = [

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
    ]
    right_widgets = [
        MultiLineWidget(key="sc_01", label="IPv4 and IPv6 Networks in CIDR Format", content_width=50, content_height=10,
                        attributes="", data=data),
        # DropdownWidget (16, 90, "dd_01", "Selection",   55, 10, "", data, ["one","two","three","four"], "three"),
    ]

    menu_widgets = [
        MenuItem(22, 2, "Validate", 13, 3, 0, menu_action_1, "context for menu 1"),
        MenuItem(22, 17, "Cancel", 7, 3, 0, menuAction2, "context for menu 2"),
        MenuItem(22, 26, "Ok-Run", 7, 3, 0, menuAction3, "context for menu 3")
    ]
    form = Form(stdscr, 45, 180, left_widgets, right_widgets, menu_widgets, data)
    form.run()


curses.wrapper(main)

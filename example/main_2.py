import sys
import os
import curses

menu = ['Home', 'Store Lookup', 'MAC Lookup', 'MAC Clear',
        'Afterhours Wi-Fi Disable/Enable', 'Exit']



requiredHeight = 15
requiredWidth = 60


# print(sys.path)
test_dir = os.path.dirname(__file__)
project_dir = os.path.dirname(os.path.dirname(__file__))
src_dir = os.path.join(project_dir, "simple_curses")
project_dir = os.path.abspath("../")
if not project_dir in sys.path:
    # print("Adding to sys.path")
    sys.path.append(project_dir)
    sys.path.append(src_dir)

from simple_curses.widget import TextWidget, IntegerWidget, FloatWidget, IPAddressWidget, IPNetworkWidget, MenuItem
from simple_curses.scrolling_widget import ScrollingWidget
from dummy_windget import DummyWidget
from simple_curses.form2 import Form2
 
def testScreenSize(stdscr):
    h, w = stdscr.getmaxyx()
    if h < requiredHeight or w < requiredWidth:
        raise Exception(
            "SCreen is too small must be at least 15 high and 60 wide")


def menuAction0(form, context):
    form.msg_info("menu action 0")

def menuAction1(form, context):
    v = form.get_values()
    s = ""
    if v is not None:
        for k in v.keys():
            s += "v[{}] = {}, ".format(k, v[k])

    form.msg_info("menu action 1 {}". format(v))
    

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
        DummyWidget("ipnet_01",     "IPNetwork ", 20, 1, "", data),
        DummyWidget("int_val_01",   "Integer   ", 20, 3, "", data),
        DummyWidget("float_val_01", "Float     ", 20, 4, "", data),
        DummyWidget("ipaddr_01",    "IPAddr    ", 20, 2, "", data),
        DummyWidget("text_01",      "Text      ", 20, 1, "", data),
    ]
    right_widgets = [
        DummyWidget("ipnet_01",     "IPNetwork ", 20, 1, "", data),
        DummyWidget("int_val_01",   "Integer   ", 20, 3, "", data),
        DummyWidget("float_val_01", "Float     ", 20, 4, "", data),
        DummyWidget("ipaddr_01",    "IPAddr    ", 20, 2, "", data),
        DummyWidget("text_01",      "Text      ", 20, 1, "", data),
    ]
    form = Form2(stdscr, 30, 100, left_widgets, right_widgets, data)
    form.run()

curses.wrapper(main)

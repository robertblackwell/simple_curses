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

from simple_curses.text_widget import TextWidget, IntegerWidget, FloatWidget, IPAddressWidget, IPNetworkWidget, TimeOfDayWidget
from simple_curses.menu import MenuItem
from simple_curses.multi_line_widget import MultiLineWidget
from simple_curses.form import Form

 
def testScreenSize(stdscr):
    h, w = stdscr.getmaxyx()
    if h < requiredHeight or w < requiredWidth:
        raise Exception(
            "SCreen is too small must be at least {} high and {} wide currently is high: {} wide: {}".format(requiredHeight, requiredWidth, h, w))


def menuAction0(form, context):
    form.msg_info("menu action 0")

def menuAction1(form, context):
    v = form.get_values()
    s = ""
    if v is not None:
        for k in v.keys():
            s += "v[{}] = {}, ".format(k, v[k])

    form.msg_info("menu action 1 {}". format(v))
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
    widgets = [ 

        IPNetworkWidget( 2,2,"ipnet_01",     "IPNetwork         ", 20, "", data),
        IntegerWidget  ( 4,2,"int_val_01",   "Integer           ", 20, "", data),
        FloatWidget    ( 6,2,"float_val_01", "Float             ", 20, "", data),
        IPAddressWidget( 8,2,"ipaddr_01",    "IPAddr            ", 20, "", data),
        TimeOfDayWidget(10,2, "tod_01",      "Time Of Day (24h) ", 20, "", data),
        TextWidget     (12,2,"text_01",      "Text              ", 20, "", data),

        MultiLineWidget(2, 90, "sc_01", "IP Networks", 55, 10, "", data),

        MenuItem(22, 2, "Validate", 13, 3, 0, menuAction1, "context for menu 1"),
        MenuItem(22, 17, "Cancel", 7, 3, 0, menuAction2, "context for menu 2"),
        MenuItem(22, 26, "Ok-Run", 7, 3, 0, menuAction3, "context for menu 3")
    ]
    form = Form(stdscr, 30, 180, widgets, data)
    form.run()

curses.wrapper(main)

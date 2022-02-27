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

from simple_curses.widget import Form, TextWidget, MenuItem
 
def testScreenSize(stdscr):
    h, w = stdscr.getmaxyx()
    if h < requiredHeight or w < requiredWidth:
        raise Exception(
            "SCreen is too small must be at least 15 high and 60 wide")


def menuAction0(context):
    x = context

def menuAction1(context):
    x = context

def menuAction2(context):
    x = context

def menuAction3(context):
    x = context



def main(stdscr):
    data = "dummy context"
    testScreenSize(stdscr)
    curses.curs_set(2)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    widgets = [ 
        TextWidget(2,2,"Widget 1st", 20,  "", data),
        TextWidget(4,2,"Widget 2nd", 20, "", data),
        TextWidget(6,2,"Widget 3rd", 20, "", data),
        TextWidget(8,2,"Widget 4th", 20, "", data),
    ]
    menus = [ 
        MenuItem("MFirst", "KEY_FN(1)", menuAction1),
        MenuItem("MSecond", "KEY_FN(2)", menuAction2),
        MenuItem("MTHird", "KEY_FN(3)", menuAction3)
    ]
    form = Form(stdscr, 20, 100, widgets, menus, data)
    form.run()

curses.wrapper(main)

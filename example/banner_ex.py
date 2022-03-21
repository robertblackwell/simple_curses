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
from simple_curses.view import AppBase, View, ViewBody, BannerView
from banner_widget import BannerWidget, HelpWidget


def testScreenSize(stdscr):
    h, w = stdscr.getmaxyx()
    if h < requiredHeight or w < requiredWidth:
        raise Exception(
            "SCreen is too small must be at least {} high and {} wide currently is high: {} wide: {}".format(
                requiredHeight, requiredWidth, h, w))


def menuAction0(form, context):
    form.msg_info("menu action 0")


def menuAction01(form, context):
    v = form.get_values()
    s = ""
    if v is not None:
        for k in v.keys():
            s += "v[{}] = {}, ".format(k, v[k])

    form.msg_info("menu action 0-1 {}".format(v))
    # run a command with elements of v as arguments


def menuAction02(form, context):
    form.msg_info("menu action 0-2")


def menuAction03(form, context):
    form.msg_info("menu action 0-3")

def menuAction11(form, context):
    v = form.get_values()
    s = ""
    if v is not None:
        for k in v.keys():
            s += "v[{}] = {}, ".format(k, v[k])

    form.msg_info("menu action 1-1 {}".format(v))
    # run a command with elements of v as arguments


def menuAction12(form, context):
    form.msg_info("menu action 1-2")


def menuAction13(form, context):
    form.msg_info("menu action 1-3")


########################################################################################################################################### 
# Here we define a class called App (name is not important - BUT MUST inherit from AppBase)
# The purpose of this class is to provide a shell inside of which we can define:
# - one or more Views
# - the arrangement of text and data entry fields inside each of those views 
#   -   the __init__() function for the custom App class must be exactly as given below
#   -   def register_views() - this function is where you define your views and their
#       component widgets.
#       NOTE: the last 2 lines of this function MUST be included:
#
#           self.views = [view_banner, view_help, view_data_entry_01]
#           return super().register_views()
#
#
########################################################################################################################################### 
class App(AppBase):
    def __init__(self, stdscr, body_height, body_width, view_widgets, view_menu_items, context, input_timeout_ms=2):
        # do not mosify this line
        super().__init__(stdscr, body_height, body_width, "context")

    def register_views(self):
        # start of customization
        self.data = "data context"
        data = self.data
        view_banner = BannerView(self, "bview_01", "Banner View", self.stdscr, self.body_win, BannerWidget())
        view_help   = BannerView(self, "help_01",  "Help   View", self.stdscr, self.body_win, HelpWidget())
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
            
        view_menu_items_01 = [ 
                MenuItem(22, 2, "Validate", 13, 3, 0, menuAction01, "context for menu 1"),
                MenuItem(22, 17, "Cancel", 7, 3, 0, menuAction02, "context for menu 2"),
                MenuItem(22, 26, "Ok-Run", 7, 3, 0, menuAction03, "context for menu 3")
            ]
        view_data_entry_01 = View(self, "view_01", "First View", self.stdscr, self.body_win, view_widgets_01, view_menu_items_01)

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
            
        view_menu_items_02 = [ 
                MenuItem(22, 2, "Validate", 13, 3, 0, menuAction11, "context for menu 1"),
                MenuItem(22, 17, "Cancel", 7, 3, 0, menuAction12, "context for menu 2"),
                MenuItem(22, 26, "Ok-Run", 7, 3, 0, menuAction13, "context for menu 3")
            ]
        view_data_entry_02 = View(self, "view_02", "Second View", self.stdscr, self.body_win, view_widgets_02, view_menu_items_02)
        # end of customization

        # next two lines are required - do not change
        self.views = [view_banner, view_help, view_data_entry_01, view_data_entry_02]
        return super().register_views()


def main(stdscr):
    data = "dummy context"
    testScreenSize(stdscr)
    curses.curs_set(2)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    form = App(stdscr, 36, 180, [], [], data)
    form.run()


curses.wrapper(main)

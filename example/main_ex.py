import sys
import os
import curses
import subprocess

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

from simple_curses import *

# from simple_curses.text_widget import TextWidget, IntegerWidget, FloatWidget, IPAddressWidget, IPNetworkWidget, \
#     TimeOfDayWidget
# from simple_curses.menu import MenuItem
# from simple_curses.multi_line_widget import MultiLineWidget
# from dropdown_widget import DropdownWidget
# from simple_curses.toggle_widget import ToggleWidget
# from simple_curses.view import AppBase, View, ViewBody, BannerView
# from banner_widget import BannerWidget, HelpWidget


def test_screen_size(stdscr):
    h, w = stdscr.getmaxyx()
    if h < requiredHeight or w < requiredWidth:
        raise Exception(
            "SCreen is too small must be at least {} high and {} wide currently is high: {} wide: {}".format(
                requiredHeight, requiredWidth, h, w))


def menu_action_0(form, context):
    form.msg_info("menu action 0")

class ActionBase:
    def __init__(self, app):
        self.app = app
    
    def exit_program(self, rc):
        sys.exit(rc)
    
    def execute_command(self, cmd_ar):
        out = subprocess.run(cmd_ar, capture_output=True)
        rc = out.returncode
        stdout_lines = out.stdout.decode("utf8").split("\n")
        stderr_lines = out.stderr.decode("utf8").split("\n")
        lines = stderr_lines + stdout_lines
        if rc == 0:
            self.app.msg_info("SUCCESS - Return is 0")
            for line in lines:
                self.app.msg_info(line)
        else:
            self.app.msg_error("FAILED - Return is {}".format(rc))
            for line in lines:
                self.app.msg_error(line)


class ActionsForFirstView(ActionBase):
    """
    This is how to encapsulate the actions for a particular view into a class.

    Have a function for each view menu item
    Note the action functions have 3 parameters, but in the menu_item class
    they are called with 2 parameters
    
    Any variables needed for these actions should be instance properties of
    the action class

    """
    def __init__(self, app):
        super().__init__(app)
        pass



    def validate(self, app, context):
        v = app.get_values()
        s = ""
        if v is not None:
            for k in v.keys():
                s += "v[{}]={} ".format(k, v[k])
        app.msg_info("menu action 0-1 {}".format(v))
        # run a command with elements of v as arguments


    def cancel(self, app, context):
        app.msg_info("exit 0-2")
        self.exit_program(0)


    def run(self, app, context):
        v = app.get_values()
        astr = ""
        args = []
        if v is not None:
            for k in v.keys():
                s =  "v[{}] = {}, ".format(k, v[k])
                args.append(s)
                astr += s

        app.msg_info("menu action 0-1 {}".format(v))
        self.execute_command(["ls", "-al", "/"])


def menu_action_11(form, context):
    v = form.get_values()
    s = ""
    if v is not None:
        for k in v.keys():
            s += "v[{}] = {}, ".format(k, v[k])

    form.msg_info("menu action 1-1 {}".format(v))
    # run a command with elements of v as arguments


def menu_action_12(form, context):
    form.msg_info("menu action 1-2")


def menu_action_13(form, context):
    form.msg_info("menu action 1-3")


#######################################################################################################################
# Here we define a class called App (name is not important - BUT MUST inherit from AppBase)
# The purpose of this class is to provide a shell inside of which we can define:
# - one or more Views
# - the arrangement of text and data entry fields inside each of those views 
#   -   the __init__() function for the custom App class must be exactly as given below
#   -   def register_views() - this function is where you define your views and their
#       component widgets.
#       NOTE: the last line of this function MUST be included:
#
#           self.views = [view_banner, view_help, view_data_entry_01]
#
#
######################################################################################################################
class App(AppBase):
    def __init__(self, stdscr, body_height, body_width, context, input_timeout_ms=2):
        # do not mosify this line
        self.action01 = ActionsForFirstView(self)
        super().__init__(stdscr, body_height, body_width, context)

    def register_views(self):
        # start of customization
        self.data = "data context"
        data = self.data
        view_banner = BannerView(self, "bview_01", "Banner View", self.stdscr, self.body_win, BannerWidget(self))
        view_help = BannerView(self, "help_01", "Help   View", self.stdscr, self.body_win, HelpWidget(self))
        view_widgets_01 = [

            IPNetworkWidget(self, "ipnet_01", "IPNetwork         ", 23, "", data),
            IntegerWidget(self, "int_val_01", "Integer           ", 23, "", data),
            FloatWidget(self, "float_val_01", "Float             ", 23, "", data),
            IPAddressWidget(self, "ipaddr_01", "IPAddr            ", 23, "", data),
            TimeOfDayWidget(self, "tod_01", "Time Of Day (24h) ", 23, "", data),
            TextWidget(self, "text_01", "Text              ", 23, "", data),
            ToggleWidget(self, "toggle_01", "Toggle            ", 3, "", data, ['ENABLED', "DISABLED"], "DISABLED"),
            IPNetworkWidget(self, "ipnet_02", "IPNetwork         ", 23, "", data),
            IntegerWidget(self, "int_val_02", "Integer           ", 23, "", data),
            FloatWidget(self, "float_val_02", "Float             ", 23, "", data),
            IPAddressWidget(self, "ipaddr_02", "IPAddr            ", 23, "", data),
            TimeOfDayWidget(self, "tod_02", "Time Of Day (24h) ", 23, "", data),
            TextWidget(self, "text_02", "Text              ", 23, "", data),
            ToggleWidget(self, "toggle_02", "Toggle            ", 3, "", data, ['ENABLED', "DISABLED"], "DISABLED"),
            IPNetworkWidget(self, "ipnet_03", "IPNetwork         ", 23, "", data),
            IntegerWidget(self, "int_val_03", "Integer           ", 23, "", data),
            FloatWidget(self, "float_val_03", "Float             ", 23, "", data),
            IPAddressWidget(self, "ipaddr_03", "IPAddr            ", 23, "", data),
            TimeOfDayWidget(self, "tod_03", "Time Of Day (24h) ", 23, "", data),
            TextWidget(self, "text_03", "Text              ", 23, "", data),
            ToggleWidget(self, "toggle_03", "Toggle            ", 3, "", data, ['ENABLED', "DISABLED"], "DISABLED"),
            IPNetworkWidget(self, "ipnet_04", "IPNetwork         ", 23, "", data),
            IntegerWidget(self, "int_val_04", "Integer           ", 23, "", data),
            FloatWidget(self, "float_val_04", "Float             ", 23, "", data),
            IPAddressWidget(self, "ipaddr_04", "IPAddr            ", 23, "", data),
            TimeOfDayWidget(self, "tod_04", "Time Of Day (24h) ", 23, "", data),
            TextWidget(self, "text_04", "Text              ", 23, "", data),
            ToggleWidget(self, "toggle_04", "Toggle            ", 3, "", data, ['ENABLED', "DISABLED"], "DISABLED"),
            MultiLineWidget(app=self, key="sc_01", label="IPv4 and IPv6 Networks in CIDR Format", content_width=50,
                            content_height=10, attributes="", data=data),
            # DropdownWidget (    "dd_01", "Selection",   55, 10, "", data, ["one","two","three","four"], "three"),
        ]

        view_menu_items_01 = [
            MenuItem(self, "Validate", 13, 3, 0, menu_action_11, "context for menu 1"),
            MenuItem(self, "Cancel", 7, 3, 0, menu_action_12, "context for menu 2"),
            MenuItem(self, "Ok-Run", 7, 3, 0, menu_action_13, "context for menu 3")
        ]
        view_data_entry_01 = View(self, "view_01", "First View", self.stdscr, self.body_win, view_widgets_01,
                                  view_menu_items_01)

        view_widgets_02 = [

            IPNetworkWidget(self, "ipnet_11",      "IPNetwork          ", 23, "", data),
            IntegerWidget(self,   "int_val_11",    "Integer            ", 23, "", data),
            FloatWidget(self,     "float_val_11",  "Float              ", 23, "", data),
            IPAddressWidget(self, "ipaddr_11",     "IPAddr             ", 23, "", data),
            TimeOfDayWidget(self, "tod_11",        "Time Of Day (24h)  ", 23, "", data),
            TextWidget(self,      "text_11",       "Text               ", 23, "", data),
            ToggleWidget(self,    "toggle_11",     "Toggle             ", 3, "", data, ['ENABLED', "DISABLED"], "DISABLED"),
            PathWidget(self,      "path_22",       "File path          ", 23, "", data),
            PathExistsWidget(self,"path_exists_22","Existing File path ", 23, "", data),
            # IntegerWidget(self, "int_val_22", "Integer           ", 20, "", data),
            # FloatWidget(self, "float_val_22", "Float             ", 20, "", data),
            MultiLineWidget(app=self, key="sc_11", label="IPv4 and IPv6 Networks in CIDR Format", content_width=50,
                            content_height=10, attributes="", data=data),
            # DropdownWidget ("dd_01", "Selection",   55, 10, "", data, ["one","two","three","four"], "three"),
        ]

        view_menu_items_02 = [
            MenuItem(self, "Validate", 13, 3, 0, self.action01.validate, "context for menu 1"),
            MenuItem(self, "Cancel", 7, 3, 0, self.action01.cancel, "context for menu 2"),
            MenuItem(self, "Ok-Run", 7, 3, 0, self.action01.run, "context for menu 3")
        ]
        view_data_entry_02 = View(self, "view_02", "Second View", self.stdscr, self.body_win, view_widgets_02,
                                  view_menu_items_02)
        # end of customization

        # the next line is required - do not change
        self.views = [view_banner, view_help, view_data_entry_01, view_data_entry_02]


def main(stdscr):
    data = "dummy context"
    test_screen_size(stdscr)
    curses.curs_set(2)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    app = App(stdscr, 36, 180, data)
    app.run()


curses.wrapper(main)

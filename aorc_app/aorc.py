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

from aorc_app.actions import AorcAction
from aorc_app.state import AorcState
from simple_curses import *

def test_screen_size(stdscr):
    h, w = stdscr.getmaxyx()
    if h < requiredHeight or w < requiredWidth:
        raise Exception(
            "SCreen is too small must be at least {} high and {} wide currently is high: {} wide: {}".format(
                requiredHeight, requiredWidth, h, w))


def menu_action_0(form, context):
    form.msg_info("menu action 0")


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
        
        self.action =  AorcAction(self)
        self.state = AorcState()

        super().__init__(stdscr, body_height, body_width, context)

    def register_views(self):
        # start of customization
        data = self.state

        view_banner = BannerView(self, "bview_01", "Banner View", self.stdscr, self.body_win, BannerWidget(self))
        view_help = BannerView(self, "help_01", "Help   View", self.stdscr, self.body_win, HelpWidget(self))

        ##########################################################
        # add prefixes with a new install
        ##########################################################
        add_prefixes_new_install_widgets = [

            TextWidget(self, "cust_name",     "Cust name           ", 23, "", data),
            TextWidget(self, "bus_ord",       "Business Ord ID     ", 23, "", data),
            ToggleWidget(self, "is_marvel",   "Is a Marvel Order   ", 3, "", data, ['No ', "Yes"], "No "),
            ToggleWidget(self, "is_dm",       "Is a DM order       ", 3, "", data, ['No ', "Yes"], "No "),
            ToggleWidget(self, "is_aorc_capitalized",       
                                              "Is aorc capitalized ", 3, "", data, ['No ', "Yes"], "No "),

            IntegerWidget(self, "nokia_entry_no",   
                                              "New install Nokia entry number ", 23, "", data, initial_value = "0"),
            IPAddressWidget(self, "next_hop", "New install Next hop IP        ", 23, "", data, initial_value = "192.168.192.168"),
                            
            MultiLineWidget(app=self, key="sc_01", label="Prefixes", content_width=50,
                            content_height=20, attributes="", data=data),
        ]

        add_prefixes_new_install_menu = [
            MenuItem(self, "Validate", 13, 3, 0, menu_action_11, "context for menu 1"),
            MenuItem(self, "Cancel", 7, 3, 0, self.action.cancel, "context for menu 2"),
            MenuItem(self, "Ok-Run", 7, 3, 0, menu_action_13, "context for menu 3")
        ]
        add_prefixes_new_install_view = View(self, "add_new_install", "Add prefix - New Install", self.stdscr, self.body_win, add_prefixes_new_install_widgets,
                                  add_prefixes_new_install_menu)

        ##########################################################
        # add prefixes but NOT with a new install
        ##########################################################
        add_prefixes_not_new_install_widgets = [

            TextWidget(self, "cust_name",     "Cust name           ", 23, "", data),
            TextWidget(self, "bus_ord",       "Business Ord ID     ", 23, "", data),
            ToggleWidget(self, "is_marvel",   "Is a Marvel Order   ", 3, "", data, ['No ', "Yes"], "No "),
            ToggleWidget(self, "is_dm",       "Is a DM order       ", 3, "", data, ['No ', "Yes"], "No "),
            ToggleWidget(self, "is_aorc_capitalized",       
                                              "Is aorc capitalized ", 3, "", data, ['No ', "Yes"], "No "),

            IntegerWidget(self, "nokia_entry_no",   
                                              "New install Nokia entry number ", 23, "", data, initial_value = "0"),
            IPAddressWidget(self, "next_hop", "New install Next hop IP        ", 23, "", data, initial_value = "192.168.192.168"),
                            
            MultiLineWidget(app=self, key="sc_01", label="Prefixes", content_width=50,
                            content_height=20, attributes="", data=data),
        ]

        add_prefixes_not_new_install_menu = [
            MenuItem(self, "Validate", 13, 3, 0, menu_action_11, "context for menu 1"),
            MenuItem(self, "Cancel", 7, 3, 0, menu_action_12, "context for menu 2"),
            MenuItem(self, "Ok-Run", 7, 3, 0, menu_action_13, "context for menu 3")
        ]
        add_prefixes_not_new_install_view = View(self, "add_not_new_install", "Add prefix - NOT - New Install", self.stdscr, self.body_win, 
                                add_prefixes_not_new_install_widgets,
                                add_prefixes_not_new_install_menu)

        ##########################################################
        # remove prefixes with a disconnect
        ##########################################################
        remove_prefixes_with_disconnect_widgets = [

            TextWidget(self, "cust_name",     "Cust name           ", 23, "", data),
            TextWidget(self, "bus_ord",       "Business Ord ID     ", 23, "", data),
            ToggleWidget(self, "is_marvel",   "Is a Marvel Order   ", 3, "", data, ['No ', "Yes"], "No "),
            ToggleWidget(self, "is_dm",       "Is a DM order       ", 3, "", data, ['No ', "Yes"], "No "),
            ToggleWidget(self, "is_aorc_capitalized",       
                                              "Is aorc capitalized ", 3, "", data, ['No ', "Yes"], "No "),

            IntegerWidget(self, "nokia_entry_no",   
                                              "New install Nokia entry number ", 23, "", data, initial_value = "0"),
            IPAddressWidget(self, "next_hop", "New install Next hop IP        ", 23, "", data, initial_value = "192.168.192.168"),
                            
            MultiLineWidget(app=self, key="sc_01", label="Prefixes", content_width=50,
                            content_height=20, attributes="", data=data),
        ]

        remove_prefixes_with_disconnect_menu = [
            MenuItem(self, "Validate", 13, 3, 0, menu_action_11, "context for menu 1"),
            MenuItem(self, "Cancel", 7, 3, 0, menu_action_12, "context for menu 2"),
            MenuItem(self, "Ok-Run", 7, 3, 0, menu_action_13, "context for menu 3")
        ]
        remove_prefixes_with_disconnect_view = View(self, "add_not_new_install", "Remove prefixes with disconnect", self.stdscr, self.body_win, 
                                remove_prefixes_with_disconnect_widgets,
                                remove_prefixes_with_disconnect_menu)

        ##########################################################
        # remove prefixes but NOT with a disconnect
        ##########################################################
        remove_prefixes_not_disconnect_widgets = [

            TextWidget(self, "cust_name",     "Cust name           ", 23, "", data),
            TextWidget(self, "bus_ord",       "Business Ord ID     ", 23, "", data),
            ToggleWidget(self, "is_marvel",   "Is a Marvel Order   ", 3, "", data, ['No ', "Yes"], "No "),
            ToggleWidget(self, "is_dm",       "Is a DM order       ", 3, "", data, ['No ', "Yes"], "No "),
            ToggleWidget(self, "is_aorc_capitalized",       
                                              "Is aorc capitalized ", 3, "", data, ['No ', "Yes"], "No "),

            IntegerWidget(self, "nokia_entry_no",   
                                              "New install Nokia entry number ", 23, "", data, initial_value = "0"),
            IPAddressWidget(self, "next_hop", "New install Next hop IP        ", 23, "", data, initial_value = "192.168.192.168"),
                            
            MultiLineWidget(app=self, key="sc_01", label="Prefixes", content_width=50,
                            content_height=20, attributes="", data=data),
        ]

        remove_prefixes_not_with_disconnect_menu = [
            MenuItem(self, "Validate", 13, 3, 0, menu_action_11, "context for menu 1"),
            MenuItem(self, "Cancel", 7, 3, 0, menu_action_12, "context for menu 2"),
            MenuItem(self, "Ok-Run", 7, 3, 0, menu_action_13, "context for menu 3")
        ]

        remove_prefixes_not_with_disconnect_view = View(self, "add_not_new_install", "Remove prefixes - NOT - with disconnect", self.stdscr, self.body_win, 
                                remove_prefixes_not_disconnect_widgets,
                                remove_prefixes_not_with_disconnect_menu)

        ##########################################################
        # aorc constants configuration
        ##########################################################
        config_widgets = [

            BlockTextWidget(self, [
                "The following are paths to files that will be created",
                "by this program"
            ]),

            PathWidget(self, "exception_file",     "Exception File Path    ", 70, "", data, initial_value='''/home/cjensen/bin/stuff/ddos2_exceptions'''),
            PathWidget(self, "v14_comand_file",    "V14 Command File Path  ", 70, "", data, initial_value='''/home/cjensen/bin/stuff/ddos2_v14_command_push'''),
            PathWidget(self, "quick_push_file",    "Quick Push File Path   ", 70, "", data, initial_value='''/home/cjensen/bin/stuff/ddos2_quick_push'''),
            PathWidget(self, "save_file",          "Save File Path         ", 70, "", data, initial_value='''/home/cjensen/bin/stuff/save'''),
            PathWidget(self, "pid_file",           "PID File Path          ", 70, "", data, initial_value='''/home/cjensen/bin/stuff/ddos2_script.pid'''),

            BlockTextWidget(self, [
                ""
            ]),


            BlockTextWidget(self, [
                "This next field is string constant used by the program NOT a file path",
            ]),

            TextWidget(self, "policy_name",        "DDOS Policy Name Constant ", 70, "", data, initial_value="ddos2-dynamic-check"),
            
        ]

# prefix = ""
# add_route = 0
# duration = 1200
# exception_file = '''/home/cjensen/bin/stuff/ddos2_exceptions'''
# v14_command_file = '''/home/cjensen/bin/stuff/ddos2_v14_command_push'''
# quick_push = '''/home/cjensen/bin/stuff/ddos2_quick_push'''
# save = '''/home/cjensen/bin/stuff/save'''
# pid_file = '''/home/cjensen/bin/stuff/ddos2_script.pid'''
# customer_name = ""
# bus_org_id = ""
# list_name = ""
# policy_name = "ddos2-dynamic-check"


        config_menu = [
            MenuItem(self, "Cancel", 7, 3, 0, menu_action_12, "context for menu 2"),
            MenuItem(self, "Save", 7, 3, 0, menu_action_13, "context for menu 3")
        ]

        config_view = View(self, "config", "AORC Config values", self.stdscr, self.body_win, 
                                config_widgets,
                                config_menu)

        # end of customization

        # the next line is required - do not change
        self.views = [
            view_banner, 
            view_help, 
            add_prefixes_new_install_view, 
            add_prefixes_not_new_install_view, 
            remove_prefixes_with_disconnect_view,
            remove_prefixes_not_with_disconnect_view,
            config_view
        ]


def main(stdscr):
    data = "dummy context"
    test_screen_size(stdscr)
    curses.curs_set(2)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    app = App(stdscr, 36, 180, data)
    app.run()


curses.wrapper(main)

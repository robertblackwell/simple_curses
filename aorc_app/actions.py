import sys
import os
import curses
import subprocess
from simple_curses import ActionBase



class AorcAction(ActionBase):
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

    def add_prefix(self, state, is_new_install):
        pass
    
    def remove_prefix(self, state, is_disconnect):
        pass


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


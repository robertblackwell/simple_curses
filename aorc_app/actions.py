import sys
import os
import curses
import subprocess
from aorc_app.state import AorcState
from simple_curses import ActionBase
from aorc_doit import *

def execute_command(app, cmd_ar):
    out = subprocess.run(cmd_ar, capture_output=True)
    rc = out.returncode
    stdout_lines = out.stdout.decode("utf8").split("\n")
    stderr_lines = out.stderr.decode("utf8").split("\n")
    lines = stderr_lines + stdout_lines
    if rc == 0:
        app.msg_info("SUCCESS - Return is 0")
        for line in lines:
            app.msg_info(line)
    else:
        app.msg_error("FAILED - Return is {}".format(rc))
        for line in lines:
            app.msg_error(line)

def view_cancel(app, view, context):
    """dont update the state, then redisplay the same view"""
    old_state = app.state
    view.set_values(old_state)
    return

def program_cancel(app, view, context):
    app.msg_info("exit")
    sys.exit(0)


def validate(self, app, view, context):
    v = app.get_values()
    s = ""
    if v is not None:
        for k in v.keys():
            s += "v[{}]={} ".format(k, v[k])
    app.msg_info("menu action 0-1 {}".format(v))
    # run a command with elements of v as arguments

def config_validate(app, view, context):
    v = app.get_values()
    s = ""
    new_state = AorcState()
    ns = {}
    if v is not None:
        for k in v.keys():
            s += "v[{}]={} ".format(k, v[k])
            setattr(new_state, k, v[k])
            ns[k] = v[k]

    app.msg_info("menu action 0-1 {}".format(v))
    return new_state

def run_config_action(app, view, context):
    new_state = config_validate(app, view, context)
    app.msg_info("Config:: {}".format(new_state.__dict__))
    #here need to update the content in each widget
    # could change the current view here if that was needed ?
    view.set_values(new_state)
    app.state = new_state

def run_add_prefix_new(app, view, context):
    new_state = validate(app, view, context)
    app.msg_info("run_add_prefixes_new:: {}".format(new_state.__dict__))
    #here need to update the content in each widget
    app.view.set_values(new_state)
    app.state = new_state

def run_add_prefix_notnew(app, view, context):
    new_state = validate(app, view, context)
    app.msg_info("run_add_prefixes_notnew:: {}".format(new_state.__dict__))
    #here need to update the content in each widget
    app.view.set_values(new_state)
    app.state = new_state

def run_remove_prefix_disconnect(app, view, context):
    new_state = validate(app, view, context)
    app.msg_info("run_remove_prefixes_disconnect:: {}".format(new_state.__dict__))
    #here need to update the content in each widget
    app.view.set_values(new_state)
    app.state = new_state

def run_remove_prefix_notdisconnect(app, view, context):
    new_state = config_validate(app, view, context)
    app.msg_info("run_remove_prefixes_notdisconnect:: {}".format(new_state.__dict__))
    #here need to update the content in each widget
    app.view.set_values(new_state)
    app.state = new_state


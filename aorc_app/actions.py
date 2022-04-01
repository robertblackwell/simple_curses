import sys
import os
import curses
import subprocess
# from aorc_app.aorc import App
from typing import Dict
from aorc_app.state import AorcState
from simple_curses import AppBase, ActionBase, View, WidgetSingleValue, WidgetListOfValues, BannerView, ResultType, WidgetValue, ViewValues
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


# def config_validate(app, view, context):
#     v = app.get_values()
#     s = ""
#     new_state = AorcState()
#     ns = {}
#     if v is not None:
#         for k in v.keys():
#             s += "v[{}]={} ".format(k, v[k])
#             setattr(new_state, k, v[k])
#             ns[k] = v[k]

#     app.msg_info("menu action 0-1 {}".format(v))
#     return new_state

def run_config_action(app, view, context):
    new_state = config_validate(app, view, context)
    app.msg_info("Config:: {}".format(new_state.__dict__))
    #here need to update the content in each widget
    # could change the current view here if that was needed ?
    view.set_values(new_state)
    app.state = new_state

def make_error_msg(view_values: ViewValues):
    msg_lines = []
    ed = {}
    for k in view_values.value_keys():
        wv = view_values[k]
        if not wv.is_ok():
            if wv.type == "WidgetSingleValue":
                ed[k] = wv
                msg = "Field with id:{} has invalid values {}".format(k, wv.get_string_value())
                msg_lines.append(msg)
            else:
                ev = []
                for v in wv.values:
                    if not v.is_ok():
                        ev.append(v.get_string_value())
                msg = "Field id:{} has invalid values {}".format(k, ev)
                msg_lines.append(msg)
                ev2 = ev

    error_text = ", ".join(msg_lines)

    return "Validation Errors {}".format(error_text)

def state_from_view_values(old_state, view_values: ViewValues):
    new_state = old_state.copy()
    vals = view_values.string_value_dict()

    new_state.__dict__.update(vals)
    return new_state


def validate(app, view: View, context):
    # this next statement also performs validation at the field level
    view_values: ViewValues = view.get_values()
    new_state = state_from_view_values(view_values)
    app.state = new_state
    if view_values.is_ok():
        app.msg_info("run_add_prefixes_new:: {}".format(new_state.__dict__))
        # here should put the actual processing that the run command is supposed to perform
        # may actually change the value of view during that processing
        view.set_values(new_state)
    else:
        app.msg_error("{}".format(make_error_msg(view_values)))
        view.set_values(new_state)

def config_validate(app, view: View, context):
    # this next statement also performs validation at the field level
    view_values: ViewValues = view.get_values()
    new_state = state_from_view_values(app.state, view_values)
    app.state = new_state
    if view_values.is_ok():
        app.msg_info("run_add_prefixes_new:: {}".format(new_state.__dict__))
        # here should put the actual processing that the run command is supposed to perform
        # may actually change the value of view during that processing
        view.set_values(new_state)
    else:
        app.msg_error("{}".format(make_error_msg(view_values)))
        view.set_values(new_state)

def run_add_prefix_new(app, view, context):
    # this next statement also performs validation at the field level
    view_values: ViewValues = view.get_values()
    new_state = state_from_view_values(app.state, view_values)
    app.state = new_state
    if view_values.is_ok():
        app.msg_info("run_add_prefixes_new:: {}".format(new_state.__dict__))
        # here should put the actual processing that the run command is supposed to perform
        # may actually change the value of view during that processing
        view.set_values(new_state)
    else:
        app.msg_error("{}".format(make_error_msg(view_values)))
        view.set_values(new_state)

def run_add_prefix_notnew(app, view, context):
    new_state = validate(app, view, context)
    app.msg_info("run_add_prefixes_notnew:: {}".format(new_state.__dict__))
    #here need to update the content in each widget
    view.set_values(new_state)
    app.state = new_state

def run_remove_prefix_disconnect(app, view, context):
    new_state = validate(app, view, context)
    app.msg_info("run_remove_prefixes_disconnect:: {}".format(new_state.__dict__))
    #here need to update the content in each widget
    view.set_values(new_state)
    app.state = new_state

def run_remove_prefix_notdisconnect(app, view, context):
    new_state = config_validate(app, view, context)
    app.msg_info("run_remove_prefixes_notdisconnect:: {}".format(new_state.__dict__))
    #here need to update the content in each widget
    view.set_values(new_state)
    app.state = new_state


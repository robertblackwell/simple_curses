import sys
import os
import curses
import subprocess

# # print(sys.path)
# test_dir = os.path.dirname(__file__)
# project_dir = os.path.dirname(os.path.dirname(__file__))
# src_dir = os.path.join(project_dir, "simple_curses")
# project_dir = os.path.abspath("../")
# if not project_dir in sys.path:
#     # print("Adding to sys.path")
#     sys.path.append(project_dir)
#     sys.path.append(src_dir)

from simple_curses import *


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



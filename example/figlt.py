import os
import sys
test_dir = os.path.dirname(__file__)
project_dir = os.path.dirname(os.path.dirname(__file__))
src_dir = os.path.join(project_dir, "simple_curses")
project_dir = os.path.abspath("../")
if not project_dir in sys.path:
    # print("Adding to sys.path")
    sys.path.append(project_dir)
    sys.path.append(src_dir)


from pyfiglet import Figlet
c = Figlet(font='big')
s = c.renderText("AORC")
x = s.split('\n')
j = "\n".join(x)
b = s == j
print(s)
for line in x:
    print(line)
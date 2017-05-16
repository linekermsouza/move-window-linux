#!/usr/bin/env python3
import subprocess
import sys

move = sys.argv[1]

def get(cmd):
    return subprocess.check_output(["/bin/bash", "-c", cmd]).decode("utf-8")
def execute(cmd):
    subprocess.call(["/bin/bash", "-c", cmd])

# screen resolutions ("raw")  
wds = [s for s in get("xrandr").split() if s.endswith("+0")]
# x-res left/right)
left =  [scr.split("x")[0] for scr in wds if scr.endswith("+0+0")]
right = [scr.split("x")[0] for scr in wds if not scr.endswith("+0+0")]
# frontmost window pos
frontmost =get("printf 0x%x "+get("xdotool getwindowfocus").strip())
frontmost = frontmost[:2]+("0" if len(frontmost) >= 9 else "00")+frontmost[2:]
f_data = [l.split() for l in get("wmctrl -lpG").splitlines() if frontmost in l][0][:6]
x = int(f_data[3])
y = int(f_data[4])
width = int(f_data[5])

if move == "left" and x >= int(left[0]):
    x = x - int(left[0])
elif move == "right" and x < int(left[0]):
    x = x + int(left[0])
# execute actions
cmd1 = "wmctrl -r :ACTIVE: -b remove,maximized_vert,maximized_horz"
cmd2 = "wmctrl -r :ACTIVE: -e 0," + str(x) + ",-1,-1,-1"

for cmd in [cmd1,cmd2]:
    execute(cmd)

cmd3 = "wmctrl -r :ACTIVE: -b add,maximized_vert,maximized_horz"
if width == int(left[0]) or width == int(right[0]):
    execute(cmd3)

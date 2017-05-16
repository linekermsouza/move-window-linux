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
left = [scr.split("x")[0] for scr in wds if scr.endswith("+0+0")]
right = [scr.split("x")[0] for scr in wds if not scr.endswith("+0+0")]
# x-positions areas
left_pos = [0, int(int(left[0])/2), int(left[0])]
right_pos = [int(int(left[0])+int(right[0])/2)] if len(right) != 0 else []
x_positions = left_pos+right_pos
# frontmost window pos
frontmost =get("printf 0x%x "+get("xdotool getwindowfocus").strip())
frontmost = frontmost[:2]+("0" if len(frontmost) >= 9 else "00")+frontmost[2:]
f_data = [l.split() for l in get("wmctrl -lG").splitlines() if frontmost in l][0][:6]
curr_pos = int(f_data[2])
area = len([x for x in x_positions if x <= curr_pos])
if move == "left":
    i = area-2; target_pos = x_positions[i] if i >= 0 else 0 
elif move == "right":
    i = area; target_pos = x_positions[area] if area < len(x_positions) else x_positions[-1]
if i >= 2:
    perc = int((100*(x_positions[-1]-x_positions[-2])/sum([int(it) for it in left+right])))
else:
    perc = int((100*(x_positions[1]-x_positions[0])/sum([int(it) for it in left+right])))
# execute actions
cmd1 = "wmctrl -r :ACTIVE: -b remove,maximized_vert,maximized_horz"
cmd2 = "wmctrl -ir "+f_data[0]+" -e 0,"+str(target_pos)+","+"30,300,300"
cmd3 = "xdotool windowsize $(xdotool getactivewindow) "+str(perc)+"% 90%"
for cmd in [cmd1, cmd2, cmd3]:
    execute(cmd)
#!/usr/bin/env python3

import subprocess
import sys
import os


def get(cmd):
    return subprocess.check_output(["/bin/bash", "-c", cmd]).decode("utf-8")


def add_keybinding(name, command, binding):

    # defining keys & strings to be used
    key = "org.gnome.settings-daemon.plugins.media-keys custom-keybindings"
    subkey1 = key.replace(" ", ".")[:-1]+":"
    item_s = "/"+key.replace(" ", "/").replace(".", "/")+"/"
    firstname = "custom"

    # get the current list of custom shortcuts
    try:
        current = eval(get("gsettings get "+key))
    except:
        current = []

    # make sure the additional keybinding mention is no duplicate
    n = 0
    while True:
        new = item_s+firstname+str(n)+"/"
        if new in current:
            n = n+1
        else:
            break
    # add the new keybinding to the list
    current.append(new)

    # create the shortcut, set the name, command and shortcut key
    cmd0 = 'gsettings set '+key+' "'+str(current)+'"'
    cmd1 = 'gsettings set '+subkey1+new+" name '" + name + "'"
    cmd2 = 'gsettings set '+subkey1+new+" command \"" + command + "\""
    cmd3 = 'gsettings set '+subkey1+new+" binding '"+binding+"'"

    for cmd in [cmd0, cmd1, cmd2, cmd3]:
        subprocess.call(["/bin/bash", "-c", cmd])


if __name__ == "__main__":
    print("ScreenEat Keybindinds Setup")
    print("===========================")
    path = os.path.dirname(os.path.realpath(__file__))
    print("Setting keybinding Ctrl+Super+P for snapshot of full screen...")
    add_keybinding("ScreenEat", "sh -c 'cd " +
                   path + " && ./ScreenEat.py'", "<Control><Super>P")
    print("Done")
    print("Setting keybinding Ctrl+Super+O for snapshot of active window...")
    add_keybinding("ScreenEat (Active)", "sh -c 'cd " +
                   path + " && ./ScreenEat.py --active'", "<Control><Super>O")
    print("Done")
    print("Setting keybinding Ctrl+Super+I for cropped snapshot...")
    add_keybinding("ScreenEat (Cropped)", "sh -c 'cd " +
                   path + " && ./ScreenEat.py --cropped'", "<Control><Super>I")
    print("Done")

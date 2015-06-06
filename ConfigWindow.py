#!/usr/bin/python3
from gi.repository import Gtk

import json
import sys, os

def LoadConfig():
    #load defaults from configuration file
    config = {}
    try:
        configstr = open("config.json").read()
        config = json.loads(configstr)
        # if 'Automatic' key doesnt exit
        if not "Automatic" in config:
            config["Automatic"] = False
    except:
        print("Couldn't load configuration file: config.json")
    return config

def SaveConfig(config):
    configstr = json.dumps(config, indent=4)
    open("config.json", "w").write(configstr)
 
def Nothing():
    pass

ChangeHandler = Nothing

"""
A configuration/settings GUI
Contains : 
    'Automatic' upload enable/disable
"""
class ConfigWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="ScreenEat Settings")
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_resizable(False)

        config = LoadConfig()

        grid = Gtk.Grid(row_homogeneous=True, column_homogeneous=True)
        grid.props.margin_top = 20
        grid.props.margin_left=20
        grid.props.margin_right = 20
        grid.props.margin_bottom = 20
        self.add(grid)

        # checkbox for upload type -> automatic or not
        check = Gtk.CheckButton("Automatic Upload")
        grid.attach(check, 0, 0, 1, 1)
        self.upload_type = check
        self.upload_type.set_active(config["Automatic"])

        okButton = Gtk.Button("Apply")
        okButton.props.margin_top = 10
        okButton.set_can_default(True)
        grid.attach(okButton, 0, 1, 1, 1)
        closeButton = Gtk.Button("Close")
        closeButton.props.margin_top = 10
        grid.attach(closeButton, 1, 1, 1, 1)

        okButton.connect("clicked", self.Apply)
        closeButton.connect("clicked", self.Close)

        self.set_default(okButton)

        # connect the main window to keypress
        self.connect("key-press-event", self.KeyPress)

    def KeyPress(self, widget, event):
        # if Escape -> 65307 is the code
        if event.keyval==65307:
            self.destroy()

    def Apply(self, w):
        config = {}
        config["Automatic"] = self.upload_type.get_active()
        SaveConfig(config)
        ChangeHandler()
        self.close()

    def Close(self, w):
        self.close()

def main():
    win = ConfigWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()

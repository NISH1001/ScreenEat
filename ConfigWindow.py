#!/usr/bin/python3
from gi.repository import Gtk

import json
import sys
import os


def load_config():
    # Load defaults from configuration file
    config = {}
    path = os.path.dirname(os.path.abspath(__file__))
    try:
        configstr = open(path + "/config.json").read()
        config = json.loads(configstr)
        config.setdefault('automatic-upload', False)
        config.setdefault('automatic-copy-url', True)
    except:
        print("Couldn't load configuration file: config.json")
    return config


def save_config(config):
    path = os.path.dirname(os.path.abspath(__file__))
    configstr = json.dumps(config, indent=4)
    open(path + "/config.json", "w").write(configstr)


def do_nothing():
    pass


change_handler = do_nothing


"""
A configuration/settings GUI
"""


class ConfigWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="ScreenEat Settings")
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_resizable(False)

        config = load_config()

        grid = Gtk.Grid(row_homogeneous=True, column_homogeneous=True)
        grid.props.margin_top = 20
        grid.props.margin_left = 20
        grid.props.margin_right = 20
        grid.props.margin_bottom = 20
        self.add(grid)

        # checkbox for upload type -> automatic or not
        check = Gtk.CheckButton("Automatic Upload")
        grid.attach(check, 0, 0, 1, 1)
        self.upload_type = check
        self.upload_type.set_active(config["automatic-upload"])

        # checkbox for url copyging -> automatic or not
        check = Gtk.CheckButton("Automatic Copy Url")
        grid.attach(check, 0, 1, 1, 1)
        self.copy_url = check
        self.copy_url.set_active(config["automatic-copy-url"])

        ok_button = Gtk.Button("Apply")
        ok_button.props.margin_top = 10
        ok_button.set_can_default(True)
        grid.attach(ok_button, 0, 2, 1, 1)
        close_button = Gtk.Button("Close")
        close_button.props.margin_top = 10
        grid.attach(close_button, 1, 2, 1, 1)

        ok_button.connect("clicked", self.apply)
        close_button.connect("clicked", lambda w: self.close())

        self.set_default(ok_button)

        # connect the main window to keypress
        self.connect("key-press-event", self.key_press)

    def key_press(self, widget, event):
        # if Escape -> 65307
        if event.keyval == 65307:
            self.close()

    def apply(self, w):
        config = {}
        config["automatic-upload"] = self.upload_type.get_active()
        config["automatic-copy-url"] = self.copy_url.get_active()
        save_config(config)
        change_handler()
        self.close()

    def on_destroy(self, w, e):
        self.close()


def main():
    win = ConfigWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()

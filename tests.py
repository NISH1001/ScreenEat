#!/usr/bin/env python3

import unittest
from screen import Screen
from config import Config
from imgur_public_uploader import ImgurPublicUploader
from crop_window import CropWindow

import gi
gi.require_version('Gtk', '3.0')  # NOQA -- disable pep8 E402 warning
from gi.repository import Gtk


class Taste(unittest.TestCase):

    def test_full_capture(self):
        image = Screen().eat()
        image.digest("~/ScreenEat/tmp", "full.jpg")

    def test_active_capture(self):
        image = Screen(active=True).eat()
        image.digest("~/ScreenEat/tmp/", "active.snapshot")

    def test_cropped_capture(self):
        # Capture a image and send it to CropWindow.
        image = Screen().eat()
        win = CropWindow(image)
        win.connect("delete-event", Gtk.main_quit)
        win.show_all()
        Gtk.main()

        if not win.user_terminated:
            # After CropWindow exists, use the rectangle to crop the image.
            image.crop(win.rect.x, win.rect.y, win.rect.width, win.rect.height)
            # Then save it.
            image.digest("~/ScreenEat/tmp/")

    def test_config(self):
        configfile = "~/ScreenEat/tmp/inner/config.json"
        secret_key = "key"
        secret_id = "id"

        # Create a new config
        # test for userexpand and recursive directory creation
        config = Config(configfile)
        config.data["id"] = secret_id
        config.data["key"] = secret_key
        config.save()

        # Open saved config
        config = Config(configfile)
        # test for integrity
        self.assertTrue(config.data["key"] == secret_key)
        self.assertTrue(config.data["id"] == secret_id)
        # test for default value in dictionary
        config.data["otherkey"]


if __name__ == "__main__":
    unittest.main()

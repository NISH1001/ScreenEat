#!/usr/bin/env python3

import unittest
import gi
gi.require_version('Gtk', '3.0')  # NOQA -- disable pep8 E402 warning
from gi.repository import Gtk

from screen_eat.windows.screen import Screen
from screen_eat.windows.crop_window import CropWindow


# NOTE: this tests are broken
class Taste(unittest.TestCase):

    def test_full_capture(self):
        image = Screen().eat()
        image.digest("/tmp/", "full.snapshot.jpg")

    def test_active_capture(self):
        image = Screen(active=True).eat()
        image.digest("/tmp/", "active.snapshot")

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
            image.digest("/tmp/")


if __name__ == "__main__":
    unittest.main()

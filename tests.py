#!/usr/bin/env python3

import unittest
from gi.repository import Gdk

from screen import Screen


class Taste(unittest.TestCase):

    def test_full_capture(self):
        image = Screen().eat()
        image.digest("test_full.jpg")

    def test_active_capture(self):
        image = Screen(active=True).eat()
        image.digest("test_active.jpg")

    def test_cropped_capture(self):
        image = Screen().eat()
        image.crop(20, 20, 200, 100)
        image.digest("test_cropped.jpg")


if __name__ == "__main__":
    unittest.main()

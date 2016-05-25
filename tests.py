#!/usr/bin/env python3

import unittest
from screen import Screen
from config import Config
from imgur_public_uploader import ImgurPublicUploader


class Taste(unittest.TestCase):

    def test_full_capture(self):
        image = Screen().eat()
        image.digest("~/ScreenEat/tmp", "full.jpg")

    def test_active_capture(self):
        image = Screen(active=True).eat()
        image.digest("~/ScreenEat/tmp/", "active.snapshot")

    def test_cropped_capture(self):
        image = Screen().eat()
        image.crop(20, 20, 200, 100)
        image.digest("~/ScreenEat/tmp")

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
        self.assertTrue(config.data["key"]==secret_key)
        self.assertTrue(config.data["id"]==secret_id)
        # test for default value in dictionary
        config.data["otherkey"]

if __name__ == "__main__":
    unittest.main()

import unittest
import pathmagic

from screeneat.config import Config


class ConfigTester(unittest.TestCase):

    configfile = "/tmp/screeneat.config.json"
    secret_key = "screeneat.secret.key"
    secret_id = "screeneat.secret.id"

    def create_config(self):
        # Create a new config
        # test for userexpand and recursive directory creation
        config = Config(self.configfile)
        config.data["id"] = self.secret_id
        config.data["key"] = self.secret_key
        config.save()

    def load_config(self):
        # Open saved config
        config = Config(self.configfile)
        # test for integrity
        self.assertTrue(config.data["key"] == self.secret_key)
        self.assertTrue(config.data["id"] == self.secret_id)
        # test for default value in dictionary
        config.data["otherkey"]

    def test_create_load_config(self):
        self.create_config()
        self.load_config()


if __name__ == "__main__":
    unittest.main()

import os
import sys
import json
from collections import defaultdict

class Config:
    """Configuration with save/load functionality."""

    def __init__(self, filename):
        self.filename = os.path.abspath(os.path.expanduser(filename))
        self.load(self.filename)

    def load(self, filename):
        """Load the configuration file, given the filename."""
        filename = os.path.abspath(os.path.expanduser(filename))
        try:
            with open(filename, "r") as f:
                dictionary = json.loads(f.read())
        except Exception as e:
            dictionary = {}
        self.data = defaultdict(str, **dictionary)

    def save(self):
        """Save the configuration file."""
        directory = os.path.dirname(self.filename)
        # Create a directory if not existing
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(self.filename, "w") as f:
            f.write(json.dumps(self.data))

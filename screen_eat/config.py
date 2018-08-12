import os
import json
from collections import defaultdict


class Config:
    """Configuration with save/load functionality."""

    def __init__(self, filename, default={}):
        self.filename = os.path.abspath(os.path.expanduser(filename))
        self.load(self.filename, default)

    # Loads configuration from a file
    # If it fails, loads the default configuration
    def load(self, filename, default):
        """Load the configuration file, given the filename."""
        filename = os.path.abspath(os.path.expanduser(filename))
        try:
            with open(filename, "r") as f:
                dictionary = json.loads(f.read())
        except Exception as e:
            dictionary = default
        self.data = defaultdict(str, **dictionary)

    # Save the configuration file
    def save(self):
        """Save the configuration file."""
        directory = os.path.dirname(self.filename)
        # Create a directory if not existing
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(self.filename, "w") as f:
            f.write(json.dumps(self.data, indent=4))

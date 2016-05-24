import os
import sys
import time
# from datetime import datetime

class Image:
    """Image representing a pixel buffer."""

    def __init__(self, pixel_buffer):
        self.pixel_buffer = pixel_buffer

    def _generate_filename(self):
        """Generate a unique filename for the image based on timestamp."""
        # timestamp = datetime.now().strftime("_%y_%m_%d_%H_%M_%S_%f")
        timestamp = "_%s" % (int(time.time() * 1000))
        return "screeneat" + timestamp + ".jpg"

    def digest(self, directory, filename=None):
        """Save image to file, with given filename and directory."""
        # make it posix and windows safe, also expand user directory
        directory = os.path.abspath(os.path.expanduser(directory))
        # Create a directory if not existing
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Generate filename using timestamp if not provided
        if not filename:
            filename = self._generate_filename()
        # Add extension if not already in the filename
        if filename[filename.rfind(".")+1:].lower() not in {'jpg', 'jpeg'}:
            filename = filename + ".jpg"
        # Join directory with the filename
        filename = os.path.join(directory, filename)

        self.pixel_buffer.savev(filename, "jpeg", (), ())

    def crop(self, x, y, width, height):
        """Crop the image to given rectangle."""

        cropped_pb = self.pixel_buffer.new_subpixbuf(x, y, width, height)
        self.pixel_buffer = cropped_pb

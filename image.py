import os
import sys
import time

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GdkPixbuf

class Image:
    """Image representing a pixel buffer."""

    def __init__(self, pixbuf):
        self.pixbuf = pixbuf

    def copy(self):
        return Image(self.pixbuf.copy())

    def generate_filename(self):
        """Generate a unique filename for the image based on timestamp."""

        timestamp = "_%s" % (int(time.time() * 1000))
        return "screeneat" + timestamp + ".jpg"

    def digest(self, directory, filename=None):
        """Save image to file, with given filename and directory."""

        # Make path posix and windows safe, expanding the user directory.
        directory = os.path.abspath(os.path.expanduser(directory))

        # Create the directory if doesn't exist.
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Generate filename using timestamp if not provided.
        if not filename:
            filename = self.generate_filename()

        # Add extension if not already in the filename.
        if filename[filename.rfind(".")+1:].lower() not in {'jpg', 'jpeg'}:
            filename = filename + ".jpg"

        # Join directory with the filename.
        filename = os.path.join(directory, filename)

        self.pixbuf.savev(filename, "jpeg", (), ())

    def crop(self, x, y, width, height):
        """Crop the image to given rectangle."""

        cropped_pb = self.pixbuf.new_subpixbuf(x, y, width, height)
        self.pixbuf = cropped_pb

    def scale(self, size=500):
        """Crop the image to certain size preserving aspect ratio."""

        ratio = self.pixbuf.get_height()/self.pixbuf.get_width()

        if ratio > 1:
            scaled_pb = self.pixbuf.scale_simple(size/ratio, size,
                                                 GdkPixbuf.InterpType.BILINEAR)
        else:
            scaled_pb = self.pixbuf.scale_simple(size, size*ratio,
                                                 GdkPixbuf.InterpType.BILINEAR)
        self.pixbuf = scaled_pb

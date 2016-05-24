from datetime import datetime


class Image:
    """Image representing a pixel buffer."""

    def __init__(self, pixel_buffer):
        self.pixel_buffer = pixel_buffer

        # Generate random default filename for this image.
        self.generate_filename()

    def generate_filename(self):
        """Generate a unique filename for the image based on timestamp."""

        suffix = datetime.now().strftime("_%y%m%d_%H%M%S")
        prefix = "screenshot"
        self.filename = prefix + suffix + ".jpg"

    def digest(self, filename=None):
        """Save image to file, optionally with given filename."""

        if filename:
            self.filename = filename
        self.pixel_buffer.savev(self.filename, "jpeg", (), ())

    def crop(self, x, y, width, height):
        """Crop the image to given rectangle."""

        cropped_pb = self.pixel_buffer.new_subpixbuf(x, y, width, height)
        self.pixel_buffer = cropped_pb

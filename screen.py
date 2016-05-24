from gi.repository import Gdk

from image import Image


class Screen:
    """Screen representing either full screen or active window."""

    def __init__(self, active=False):
        # Get the window.
        if active:
            self.window = Gdk.Screen.get_default().get_active_window()
        else:
            self.window = Gdk.get_default_root_window()

    def eat(self):
        """Capture the screenshot and return the image."""

        x, y, w, h = self.window.get_geometry()
        pixbuf = Gdk.pixbuf_get_from_window(self.window, x, y, w, h)

        # Return Image object with captured screenshot.
        return Image(pixbuf)

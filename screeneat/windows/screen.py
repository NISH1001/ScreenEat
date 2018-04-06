import gi
gi.require_version('Gdk', '3.0')  # NOQA -- disable pep8 E402 warning
from gi.repository import Gdk
from screeneat.image import Image


class Screen:
    """Screen representing either full screen or active window."""

    def __init__(self, active=False):
        # Get the window.
        self.screen = Gdk.Screen.get_default()
        self.root_window = self.screen.get_root_window()
        active_window = self.screen.get_active_window()

        monitor = self.screen.get_monitor_at_window(active_window)
        self.area = self.screen.get_monitor_geometry(monitor)

        if active:
            self.window = active_window
        else:
            self.window = self.root_window

    def eat(self):
        """Capture the screenshot and return the image."""

        _, clip_area = self.window.get_frame_extents().intersect(self.area)
        pixbuf = Gdk.pixbuf_get_from_window(self.root_window,
                                            clip_area.x, clip_area.y,
                                            clip_area.width,
                                            clip_area.height)

        # Return Image object with captured screenshot.
        return Image(pixbuf)

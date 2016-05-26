import gi
gi.require_version('Gtk', '3.0')  # NOQA -- disable pep8 E402 warning
gi.require_version('Gdk', '3.0')  # NOQA -- disable pep8 E402 warning
from gi.repository import Gtk
from gi.repository import Gdk


class MouseButtons:
    LEFT_BUTTON = 1
    RIGHT_BUTTON = 3


class CropWindow(Gtk.Window):
    """Window displaying the captured screenshot for cropping."""

    def __init__(self, image):
        Gtk.Window.__init__(self, title="")

        # Create fullscreen window.
        self.fullscreen()
        self.image = image
        self.user_terminated = False

        # Add an overlay with the given image.
        self.drawing_area = Gtk.DrawingArea()
        self.add(self.drawing_area)
        self.drawing_area.connect("draw", self._on_draw)

        # Intialize cropping rectangle to (0,0,0,0).
        self.rect = Gdk.Rectangle()
        self.cropping = False

        # Attach mouse and keyboard events.
        self.drawing_area.set_events(Gdk.EventMask.EXPOSURE_MASK |
                                     Gdk.EventMask.BUTTON_PRESS_MASK |
                                     Gdk.EventMask.BUTTON_RELEASE_MASK |
                                     Gdk.EventMask.POINTER_MOTION_MASK)

        self.drawing_area.connect("button-press-event", self._on_mouse_down)
        self.drawing_area.connect("motion_notify_event", self._on_mouse_move)
        self.drawing_area.connect("button-release-event", self._on_mouse_up)
        self.connect("key-press-event", self._on_key_press)

    def _on_draw(self, widget, context):
        # First the draw the image.
        Gdk.cairo_set_source_pixbuf(context, self.image.pixel_buffer, 0, 0)
        context.paint()

        # Next draw the cropping rectangle.
        if self.cropping:
            # The fill
            context.set_source_rgba(0.2, 0.5, 0.9, 0.3)
            context.rectangle(self.rect.x, self.rect.y,
                              self.rect.width, self.rect.height)
            context.fill()

            # The border
            context.set_source_rgba(0.2, 0.5, 0.9, 1)
            context.rectangle(self.rect.x, self.rect.y,
                              self.rect.width, self.rect.height)
            context.stroke()

        return False

    def _on_mouse_down(self, widget, event):
        # Set the initial mouse position.
        if event.button == MouseButtons.LEFT_BUTTON:
            self.starting_x = event.x
            self.starting_y = event.y
            self.cropping = True

    def _on_mouse_move(self, widget, event):
        if self.cropping:
            # Update the cropping rectangle.
            self._end_rect(event.x, event.y)

    def _on_mouse_up(self, widget, event):
        if self.cropping and event.button == MouseButtons.LEFT_BUTTON:
            # Update the cropping rectangle.
            self._end_rect(event.x, event.y)

            # Stop cropping and close the window.
            self.cropping = False
            self.close()

    def _end_rect(self, x, y):
        x1, y1 = self.starting_x, self.starting_y
        x2, y2 = x, y

        self.rect.x = x1 if x1 < x2 else x2
        self.rect.y = y1 if y1 < y2 else y2
        self.rect.width = abs(x1 - x2)
        self.rect.height = abs(y1 - y2)

        self.queue_draw()

    def _on_key_press(self, widget, event):
        # Exit on escape.
        if event.keyval == 65307:
            self.close()
            self.user_terminated = True

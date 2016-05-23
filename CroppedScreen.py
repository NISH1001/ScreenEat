#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk
import cairo

from Screenshot import Screenshot


class MouseButtons:
    LEFT_BUTTON = 1
    RIGHT_BUTTON = 3


class CroppedScreen(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="")

        # Create a fullscreen window and add drawing area
        self.fullscreen()
        self.drawing_area = Gtk.DrawingArea()
        self.add(self.drawing_area)

        # Set some variables
        self.draw = False
        self.rect_x = self.rect_width = 0
        self.rect_y = self.rect_height = 0

        # Connect events

        self.drawing_area.connect('draw', self.on_draw)
        self.drawing_area.set_events(Gdk.EventMask.EXPOSURE_MASK |
                                     Gdk.EventMask.BUTTON_PRESS_MASK |
                                     Gdk.EventMask.BUTTON_RELEASE_MASK |
                                     Gdk.EventMask.POINTER_MOTION_MASK)

        self.drawing_area.connect("button-press-event", self.mouse_down)
        self.drawing_area.connect("motion_notify_event", self.mouse_move)
        self.drawing_area.connect("button-release-event", self.mouse_release)
        self.connect("key-press-event", self.key_press)

        # Set mouse cursor type to CROSS/PLUS
        self.set_cursor(Gdk.Cursor(Gdk.CursorType.CROSS))

        # Take full screenshot to show in drawing area
        self.shot = Screenshot()
        self.pixel_buffer = self.shot.take_shot(0, 0, self.shot.full_width,
                                           self.shot.full_height, self.shot.root_window)

    def set_cursor(self, cursor):
        self.get_root_window().set_cursor(cursor)

    def on_draw(self, wid, cr):
        # Draw the full screen shot
        Gdk.cairo_set_source_pixbuf(cr, self.pixel_buffer, 0, 0)
        cr.paint()

        # rectangle overlay
        cr.set_source_rgba(1, 1, 1, 0.1)
        cr.rectangle(0, 0,
                     self.shot.full_width, self.shot.full_height)
        cr.fill()

        # Draw rectangle for current selection
        if self.draw:
            cr.set_source_rgba(0.5, 0.5, 0.5, 0.3)
            cr.rectangle(self.rect_x, self.rect_y,
                         self.rect_width, self.rect_height)
            cr.fill()
        return True

    def mouse_down(self, w, e):
        if e.button == MouseButtons.LEFT_BUTTON:
            self.rect_x = e.x
            self.rect_y = e.y
            self.init_x = e.x
            self.init_y = e.y
            self.draw = True

    def mouse_release(self, w, e):
        if e.button == MouseButtons.LEFT_BUTTON:
            y = e.y
            x = e.x
            self.get_rect(x, y)
            self.draw = False
            self.close()

            # restore the cursor type
            self.set_cursor(Gdk.Cursor(Gdk.CursorType.LEFT_PTR))

    def mouse_move(self, w, e):
        x = e.x
        y = e.y
        if self.draw:
            self.get_rect(x, y)
            self.queue_draw()

    # Calculate rectangle to draw selection
    def get_rect(self, x, y):
        x1 = self.init_x
        y1 = self.init_y
        self.rect_width = abs(x-x1)
        self.rect_height = abs(y-y1)

        if x < x1 and y < y1:
            self.rect_x = x
            self.rect_y = y
        elif x < x1 and y > y1:
            self.rect_x = x
        elif x > x1 and y < y1:
            self.rect_y = y
        else:
            pass

    def key_press(self, widget, event):
        # if Escape -> 65307 is the code
        if event.keyval == 65307:
            self.close()
            self.set_cursor(Gdk.Cursor(Gdk.CursorType.LEFT_PTR))


def main():
    win = CroppedScreen()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()

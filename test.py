#!/usr/bin/python3

from gi.repository import Gtk
from gi.repository import Gdk
import cairo

class MouseButtons:
    LEFT_BUTTON =1
    RIGHT_BUTTON = 3

class CroppedScreen(Gtk.Window):
    
    def __init__(self):
        self.draw = False

        self.rect_x = self.rect_width = self.rect_y \
            = self.rect_height = 0

        Gtk.Window.__init__(self, title="")
        self.fullscreen()
        self.set_opacity(0.05)

        self.drawing_area = Gtk.DrawingArea()

        self.drawing_area.connect('draw', self.on_draw)

        self.drawing_area.set_events(Gdk.EventMask.EXPOSURE_MASK | \
            Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.BUTTON_RELEASE_MASK \
            | Gdk.EventMask.POINTER_MOTION_MASK)


        self.drawing_area.connect("button-press-event", self.on_button_press)
        self.drawing_area.connect("motion_notify_event", self.on_mouse_move)
        self.drawing_area.connect("button-release-event", self.on_button_release)

        self.add(self.drawing_area)

        self.show_all()


    def on_draw(self, wid, cr):#draws the rectangle
        cr.set_source_rgba(0,0,0,0.5)
        cr.rectangle(self.rect_x, self.rect_y, self.rect_width, self.rect_height)
        cr.fill()


    def on_button_press(self, w, e):
        self.draw=True
        if e.type==Gdk.EventType.BUTTON_PRESS \
            and e.button == MouseButtons.LEFT_BUTTON:
            self.rect_x= e.x
            self.rect_y = e.y
            return

    def on_button_release(self, w, e):
        if e.type==Gdk.EventType.BUTTON_RELEASE \
            and e.button == MouseButtons.LEFT_BUTTON:
            y=e.y
            x=e.x
            self.get_rect(x, y)
            self.drawing_area.queue_draw()
        self.draw = False

    def on_mouse_move(self, w, e):
        x = e.x
        y = e.y
        if self.draw:
            self.get_rect(x, y)
            self.drawing_area.queue_draw()

    # here width of rectangle and proper starting point is found
    def get_rect(self, x, y):
        x1 = self.rect_x
        y1 = self.rect_y
        self.rect_width = abs(x-x1)
        self.rect_height = abs(y-y1)
        if x<x1 and y<y1:#means rectangle is drawn from down right to up left
            # change start point
            self.rect_x = x
            self.rect_y = y
        elif x<x1 and y>y1:
            self.rect_x = x
        elif x>x1 and y<y1:
            self.rect_y = y
        else:
            pass


win = CroppedScreen()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()

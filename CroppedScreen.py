#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk
import cairo

class MouseButtons:
    LEFT_BUTTON =1
    RIGHT_BUTTON = 3

"""
Cropped Window UI
Contains : 

rect_x, rect_y          - x,y top-left position of cropped region
rect_width, rect_height - width,height of the rectangular cropped region 


"""
class CroppedScreen(Gtk.Window):
    
    def __init__(self):
        self.draw = False

        self.rect_x = self.rect_width = self.rect_y \
            = self.rect_height = 0

        Gtk.Window.__init__(self, title="")
        self.fullscreen()
        self.set_opacity(0.25)

        self.drawing_area = Gtk.DrawingArea()

        self.drawing_area.connect('draw', self.OnDraw)

        self.drawing_area.set_events(Gdk.EventMask.EXPOSURE_MASK | \
            Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.BUTTON_RELEASE_MASK \
            | Gdk.EventMask.POINTER_MOTION_MASK)


        self.drawing_area.connect("button-press-event", self.OnButtonPress)
        self.drawing_area.connect("motion_notify_event", self.OnMouseMove)
        self.drawing_area.connect("button-release-event", self.OnButtonRelease)

        self.add(self.drawing_area)

        # connect the main window to keypress
        self.connect("key-press-event", self.KeyPress)

        # set mouse cursor type to CROSS/PLUS
        self.SetCursor(Gdk.Cursor(Gdk.CursorType.CROSS))

    def SetCursor(self, cursor):
        self.get_root_window().set_cursor(cursor)

    def OnDraw(self, wid, cr):#draws the rectangle
        cr.set_source_rgba(0,0,0,0.5)
        cr.rectangle(self.rect_x, self.rect_y, self.rect_width, self.rect_height)
        cr.fill()


    def OnButtonPress(self, w, e):
        self.draw=True
        if e.type==Gdk.EventType.BUTTON_PRESS \
            and e.button == MouseButtons.LEFT_BUTTON:
            self.rect_x= e.x
            self.rect_y = e.y
            self.init_x = e.x
            self.init_y = e.y
            return

    def OnButtonRelease(self, w, e):
        if e.type==Gdk.EventType.BUTTON_RELEASE and e.button == MouseButtons.LEFT_BUTTON:
            y=e.y
            x=e.x
            self.GetRect(x, y)
            self.draw = False
            self.drawing_area.destroy()
            self.close()

            # restore the cursor type
            self.SetCursor(Gdk.Cursor(Gdk.CursorType.LEFT_PTR))

    def OnDestroy(self, w, e):
        self.close()

    def OnMouseMove(self, w, e):
        x = e.x
        y = e.y
        if self.draw:
            self.GetRect(x, y)
            self.drawing_area.queue_draw()

    # here width of rectangle and proper starting point is found
    def GetRect(self, x, y):
        x1 = self.init_x
        y1 = self.init_y
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
    def KeyPress(self, widget, event):
        # if Escape -> 65307 is the code
        if event.keyval==65307:
            self.SetCursor(Gdk.Cursor(Gdk.CursorType.LEFT_PTR))
            self.close()

def main():
    win = CroppedScreen()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__=="__main__":
    main()

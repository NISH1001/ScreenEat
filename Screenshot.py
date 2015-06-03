#!/usr/bin/env python3

from gi.repository import Gdk
import time
import re

# own exception class
class ManualError(Exception):
    def __init__(self, args):
        self.args = args
    
    def display(self):
        print(''.join(self.args))

"""
Simple screen shot class
TakeShot : returns a pixel buffer
SaveShot : accepts pixelbuffer and filename 
"""
class Screenshot(object):
    def __init__(self):
        self.root_window = Gdk.get_default_root_window()
        self.x, self.y, self.full_width, self.full_height = self.root_window.get_geometry()

    def TakeShot(self, x,y, width, height):
        pixel_buffer = Gdk.pixbuf_get_from_window(self.root_window, x, y, width, height)
        return pixel_buffer

    def SaveShot(self, pixel_buffer, filename):
        # if no filename, create it using timestamp
        if not filename:
            filename = re.sub(r'\.', '', str(time.time()))
        try:
            if not pixel_buffer:
                raise ManualError("no pixel buffer. please take screenshot at first")
            else:
                pixel_buffer.savev(str(filename) + ".jpg", "jpeg", (), ())
        except ManualError as err:
            err.display()
            return False
        return True


def main():
    shot = Screenshot()
    pb = shot.TakeShot(0, 0, shot.full_width, shot.full_height)
    shot.SaveShot(pb, "test")

if __name__=="__main__":
    main()

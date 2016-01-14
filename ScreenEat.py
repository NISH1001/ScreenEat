#!/usr/bin/env python3

import platform, sys, os
import time
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject
import ConfigWindow
from Screenshot import Screenshot
from threading import Thread
from ImgurUploader import ImgurUploader
from CroppedScreen import CroppedScreen
import time

"""
Main GUI for our screenshot
Contains Three section

Section 1 : Image Preview of the shot
Section 2 : Utilites like 'save image', 'copy to clipboard' , 'settings UI'
Section 3 : Upload Section like 'upload the image', 'get the sharable link'

If 'automatic' upload is enabled :
    screenshot is automatically uploaded and
    a sharable link is provided if successful
"""
class ScreenEat(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="ScreenEat")
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_resizable(False)

        grid = Gtk.Grid(row_homogeneous=False, column_homogeneous=False)
        grid.props.margin_top = 5
        grid.props.margin_right = 5
        grid.props.margin_left = 5
        grid.props.margin_bottom = 5
        self.add(grid)
        self.grid = grid

        # take the shot immediately after invoke
        # take shot, considering --active argument
        shot = Screenshot()
        arguments = sys.argv[1::]
        if "--active" in arguments:
            pixel_buffer = shot.TakeShot(0,0, shot.active_width,
                    shot.active_height, shot.active_window)
            imgwidth = shot.active_width
            imgheight = shot.active_height
        elif "--cropped" in arguments:
            win = CroppedScreen()
            win.connect("delete-event", Gtk.main_quit)
            win.set_modal(True)
            win.set_keep_above(True)
            win.show_all()
            Gtk.main()
            time.sleep(0.2)
            pixel_buffer = shot.TakeShot(win.rect_x, win.rect_y,
                    win.rect_width, win.rect_height, shot.root_window)
            imgwidth = win.rect_width
            imgheight = win.rect_height
        else:
            pixel_buffer = shot.TakeShot(0,0, shot.full_width,
                    shot.full_height, shot.root_window)
            imgwidth = shot.full_width
            imgheight = shot.full_height

        # save shot for future
        shot.SaveShot(pixel_buffer, "")
        self.filename = shot.filename
        self.url = ""

        # Create image preview
        ratio = imgheight/imgwidth

        if ratio > 1:
            scaled = pixel_buffer.scale_simple(500/ratio,500,
                    GdkPixbuf.InterpType.BILINEAR)
        else:
            scaled = pixel_buffer.scale_simple(500,500*ratio,
                    GdkPixbuf.InterpType.BILINEAR)


        self.pixel_buffer = pixel_buffer
        image = Gtk.Image().new_from_pixbuf(scaled)
        self.image = image

        # create upload section:
        upload_section = Gtk.Box(spacing = 5)
        upload_section.props.margin_top = 5
        self.upload_section = upload_section

        # create buttons for upload section:
        button_upload = Gtk.Button(label="Upload")
        button_upload.connect("clicked", self.Upload)
        self.button_upload = button_upload
        upload_section.add(button_upload)

        # create buttons for copy section:
        button_copyclipboard = Gtk.Button(label="Copy url")
        button_copyclipboard.connect("clicked", self.CopyUrl)
        self.button_copyclipboard = button_copyclipboard
        upload_section.add(button_copyclipboard)

        # Create misc section:
        misc_section = Gtk.Box(spacing=5)
        misc_section.props.margin_top = 5
        misc_section.props.halign = Gtk.Align.END

        # Create buttons for misc section
        button_save = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_SAVE_AS))
        button_save.set_tooltip_text("Save image (Ctrl+S)")
        button_save.connect("clicked", self.ImageSave, pixel_buffer)
        misc_section.add(button_save)

        button_copy = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_COPY))
        button_copy.set_tooltip_text("Copy image to Clipboard")
        button_copy.connect("clicked", self.ImageCopy, pixel_buffer)
        misc_section.add(button_copy)

        button_settings = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_PREFERENCES))
        button_settings.set_tooltip_text("Settings")
        button_settings.connect("clicked", self.Configuration)
        misc_section.add(button_settings)

        # Create notification label
        label_status = Gtk.Label("ScreenEat")
        label_status.set_margin_top(5)
        label_status.set_alignment(xalign=0.5, yalign=0.5)
        label_status.props.width_chars = 24
        self.label_status = label_status

        # attach to grid
        grid.attach(image, 0, 0, 3, 1)
        grid.attach_next_to(upload_section, image,
                Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(label_status, upload_section,
                Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(misc_section, label_status,
                Gtk.PositionType.RIGHT, 1, 1)

        # connect the main window to keypress
        self.connect("key-press-event", self.KeyPress)
        self.connect("delete-event", Gtk.main_quit)

        self.show_all()

        config = ConfigWindow.LoadConfig()
        # if automatic upload then start uploading now
        if (config["automatic"]):
            self.Upload(None)
        self.button_copyclipboard.hide()


    def Configuration(self, widget):
        win = ConfigWindow.ConfigWindow()
        win.set_modal(True)
        win.show_all()

    def KeyPress(self, widget, event):
        # if Escape -> 65307 is the code
        keyval = event.keyval
        keyname = Gdk.keyval_name(keyval)
        ctrl = event.state & Gdk.ModifierType.CONTROL_MASK
        if keyname=="Escape":
            Gtk.main_quit()
        if ctrl and keyname=="s":
            self.ImageSave(widget, self.pixel_buffer)

    def CopyUrl(self, widget):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(self.url, -1)
        clipboard.store()

    def Upload(self, widget):
        thread = Thread(target=self.StartUploading)
        thread.start()

    def StartUploading(self):
        Gdk.threads_enter()
        self.label_status.set_text("Upload in Progress")
        self.button_upload.set_sensitive(False)
        Gdk.threads_leave()

        uploader = ImgurUploader()
        result = uploader.Upload(self.filename)
        # print(result)
        Gdk.threads_enter()
        if result['success']:
            self.url = result['link']
            self.label_status.set_markup("<a href='" + result['link']+"'>" + result['link'] + "</a>")
            self.button_upload.hide()
            self.button_upload.set_sensitive(True)
            self.button_copyclipboard.show()
        else:
            self.label_status.set_text("Upload Failed!")
            self.button_upload.set_sensitive(True)
        Gdk.threads_leave()

    def ImageCopy(self, widget, pixbuf):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_image(pixbuf)
        clipboard.store()

    def ImageSave(self, widget, pixbuf):
        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
                    Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL,
                    Gtk.ResponseType.CANCEL, "Save", Gtk.ResponseType.OK))

        filter_jpg = Gtk.FileFilter()
        filter_jpg.set_name("JPEG images")
        filter_jpg.add_pattern("*.jpg")
        dialog.add_filter(filter_jpg)
        dialog.set_default_size(50,50)
        dialog.set_do_overwrite_confirmation(True)
        filename = time.strftime("%Y-%m-%d %H:%M:%S.jpg")
        dialog.set_current_name(filename)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            if "." not in filename:
                filename += ".jpg"
            print(dialog.get_filename())
            shot = Screenshot()
            shot.SaveShot(pixbuf, filename)
        dialog.destroy()

def main():
    GObject.threads_init()
    if platform.system() == 'Linux':
        Gdk.threads_init()

    win = ScreenEat()
    Gdk.threads_enter()
    Gtk.main()
    Gdk.threads_leave()
    try:
        os.remove(win.filename)
    except:
        pass

if __name__ == "__main__":
    main()

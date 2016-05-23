#!/usr/bin/env python3

import platform
import sys
import os
import time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject
import ConfigWindow
from Screenshot import Screenshot, ManualError
from threading import Thread
from ImgurUploader import ImgurUploader
from CroppedScreen import CroppedScreen
import time


"""
Main ScreenEat GUI
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

        # Take shot, considering provided arguments
        shot = Screenshot()
        arguments = sys.argv[1::]

        if "--cropped" in arguments:
            win = CroppedScreen()
            win.connect("delete-event", Gtk.main_quit)
            win.set_modal(True)
            win.set_keep_above(True)
            win.show_all()

            Gdk.threads_enter()
            Gtk.main()
            Gdk.threads_leave()
            # If no rectangle is drawn, no need to get a screenshot
            if (win.rect_width * win.rect_height == 0):
                raise ManualError("No crop rectangle defined. Exiting.")

            buff = win.pixel_buffer
            pixel_buffer = buff.new_subpixbuf(win.rect_x, win.rect_y,
                                              win.rect_width, win.rect_height)
        elif "--active" in arguments:
            pixel_buffer = shot.take_shot(0, 0, shot.active_width,
                                          shot.active_height,
                                          shot.active_window)
        else:
            pixel_buffer = shot.take_shot(0, 0, shot.full_width,
                                          shot.full_height, shot.root_window)

        # save shot for future, if fails then exit
        shot.save_shot(pixel_buffer, "")

        self.filename = shot.filename
        self.url = ""

        # Create image preview
        ratio = pixel_buffer.get_height()/pixel_buffer.get_width()

        if ratio > 1:
            scaled = pixel_buffer.scale_simple(500/ratio, 500,
                                               GdkPixbuf.InterpType.BILINEAR)
        else:
            scaled = pixel_buffer.scale_simple(500, 500*ratio,
                                               GdkPixbuf.InterpType.BILINEAR)

        self.pixel_buffer = pixel_buffer
        image = Gtk.Image().new_from_pixbuf(scaled)
        self.image = image

        # create upload section:
        upload_section = Gtk.Box(spacing=5)
        upload_section.props.margin_top = 5
        self.upload_section = upload_section

        # create buttons for upload section:
        button_upload = Gtk.Button(label="Upload")
        button_upload.connect("clicked", self.upload)
        self.button_upload = button_upload
        upload_section.add(button_upload)

        # create buttons for copy section:
        button_copyurl = Gtk.Button(label="Copy url")
        button_copyurl.connect("clicked", self.copy_url)
        self.button_copyurl = button_copyurl
        upload_section.add(button_copyurl)

        # Create misc section:
        misc_section = Gtk.Box(spacing=5)
        misc_section.props.margin_top = 5
        misc_section.props.halign = Gtk.Align.END

        # Create buttons for misc section
        button_save = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_SAVE_AS))
        button_save.set_tooltip_text("Save image (Ctrl+S)")
        button_save.connect("clicked", self.save_image, pixel_buffer)
        misc_section.add(button_save)

        button_copy = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_COPY))
        button_copy.set_tooltip_text("Copy image to Clipboard")
        button_copy.connect("clicked", self.copy_image, pixel_buffer)
        misc_section.add(button_copy)

        button_settings =\
            Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_PREFERENCES))
        button_settings.set_tooltip_text("Settings")
        button_settings.connect("clicked", self.show_config)
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
        self.connect("key-press-event", self.key_press)
        self.connect("delete-event", Gtk.main_quit)

        self.show_all()

        self.button_copyurl.hide()

        # if automatic upload then start uploading now
        config = ConfigWindow.load_config()
        if (config["automatic-upload"]):
            self.upload(None)


    def show_config(self, widget):
        win = ConfigWindow.ConfigWindow()
        win.set_modal(True)
        win.show_all()

    def key_press(self, widget, event):
        # if Escape -> 65307 is the code
        keyval = event.keyval
        keyname = Gdk.keyval_name(keyval)
        ctrl = event.state & Gdk.ModifierType.CONTROL_MASK
        if keyname == "Escape":
            Gtk.main_quit()
        if ctrl and keyname == "s":
            self.save_image(widget, self.pixel_buffer)

    def copy_url(self, widget):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(self.url, -1)
        clipboard.store()

    def upload(self, widget):
        thread = Thread(target=self.start_uploading)
        thread.start()

    def start_uploading(self):
        Gdk.threads_enter()
        self.label_status.set_text("Upload in Progress")
        self.button_upload.set_sensitive(False)
        Gdk.threads_leave()

        uploader = ImgurUploader()
        result = uploader.upload(self.filename)
        # print(result)
        Gdk.threads_enter()
        if result['success']:
            self.url = result['link']
            self.label_status.set_markup("<a href='" + result['link']+"'>" +
                                         result['link'] + "</a>")
            self.button_upload.hide()
            self.button_upload.set_sensitive(True)
            self.button_copyurl.show()
            config = ConfigWindow.load_config()
            if config["automatic-copy-url"]:
                self.copy_url(None)
        else:
            self.label_status.set_text("Upload Failed!")
            self.button_upload.set_sensitive(True)
        Gdk.threads_leave()

    def copy_image(self, widget, pixbuf):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_image(pixbuf)
        clipboard.store()

    def save_image(self, widget, pixbuf):
        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        "Save", Gtk.ResponseType.OK))

        filter_jpg = Gtk.FileFilter()
        filter_jpg.set_name("JPEG images")
        filter_jpg.add_pattern("*.jpg")
        dialog.add_filter(filter_jpg)
        dialog.set_default_size(50, 50)
        dialog.set_do_overwrite_confirmation(True)
        filename = time.strftime("%Y-%m-%d %H:%M:%S.jpg")
        dialog.set_current_name(filename)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            if "." not in filename:
                filename += ".jpg"
            print("Saving screenshot as", dialog.get_filename())
            shot = Screenshot()
            shot.save_shot(pixbuf, filename)
        dialog.destroy()


def main():
    GObject.threads_init()
    if platform.system() == 'Linux':
        Gdk.threads_init()

    try:
        win = ScreenEat()
        Gdk.threads_enter()
        Gtk.main()
        Gdk.threads_leave()
        os.remove(win.filename)
    except OSError:
        pass
    except ManualError as e:
        e.display()
        pass


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import platform, sys, os
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

        grid = Gtk.Grid(row_homogeneous=True, column_homogeneous=False)
        grid.props.margin_top = 20
        grid.props.margin_right = 20
        grid.props.margin_left = 10
        grid.props.margin_bottom = 10
        self.add(grid)

        # take the shot immediately after invoke
        shot = Screenshot()

        ''' span : from col=0, row=0, to col=1, row=4 '''
        imageprev= Gtk.Label("imagepreview")

        # take shot, considering --active argument
        arguments = sys.argv[1::]
        if "--active" in arguments:
            pixel_buffer = shot.TakeShot(0,0, shot.active_width, shot.active_height, shot.active_window)
            imgwidth = shot.active_width
            imgheight = shot.active_height

        elif "--cropped" in arguments:
            win = CroppedScreen()
            win.connect("delete-event", Gtk.main_quit)
            win.set_modal(True)
            win.set_keep_above(True)
            win.show_all()
            Gtk.main()
            time.sleep(0.1)
            pixel_buffer = shot.TakeShot(win.rect_x, win.rect_y, win.rect_width, win.rect_height, shot.root_window)
            imgwidth = win.rect_width
            imgheight = win.rect_height

        else:
            pixel_buffer = shot.TakeShot(0,0, shot.full_width, shot.full_height, shot.root_window)
            imgwidth = shot.full_width
            imgheight = shot.full_height
        
        if imgheight > imgwidth:
            scaled = pixel_buffer.scale_simple(200*imgwidth/imgheight,200, GdkPixbuf.InterpType.BILINEAR)
        else:
            scaled = pixel_buffer.scale_simple(300,300*imgheight/imgwidth, GdkPixbuf.InterpType.BILINEAR)

        self.pixel_buffer = pixel_buffer
        image = Gtk.Image().new_from_pixbuf(scaled)
        grid.attach(image, 0, 0, 1, 4)

        # save shot for future
        shot.SaveShot(pixel_buffer, "")
        self.filename = shot.filename

        box_buttons = Gtk.Box(spacing=10)
        box_buttons.props.margin_top = 10
        box_buttons.props.margin_left = 10

        #button_save = Gtk.Button(label="Save To File")
        button_save = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_SAVE_AS))
        button_save.set_tooltip_text("Save image (Ctrl+S)")
        button_save.connect("clicked", self.ImageSave, pixel_buffer) #pixel buffer is passed
        box_buttons.add(button_save)

        #button_copy = Gtk.Button(label="Copy Image To Clipboard")
        button_copy = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_COPY))
        button_copy.set_tooltip_text("Copy image to Clipboard")
        button_copy.connect("clicked", self.ImageCopy, pixel_buffer)
        box_buttons.add(button_copy)

        button_settings = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_PREFERENCES))
        button_settings.set_tooltip_text("Settings")
        button_settings.connect("clicked", self.Configuration)
        box_buttons.add(button_settings)

        box_buttons.props.halign = Gtk.Align.CENTER
        grid.attach(box_buttons, 2, 3, 3, 1)

        # create all 3 upload sections:
        uploadSection1 = Gtk.Box(spacing = 10)
        button_upload = Gtk.Button(label="Upload")
        button_upload.connect("clicked", self.Upload)
        uploadSection1.pack_start(button_upload, expand=True, fill=True, padding=5)
        uploadSection1.props.margin_left = 10
        uploadSection1.props.margin_top = 10

        uploadSection2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 10)
        spinner = Gtk.Spinner()
        spinner.start()
        uploadSection2.add(spinner)
        label_uploading = Gtk.Label("Uploading...")
        uploadSection2.add(label_uploading)
        uploadSection2.props.margin_left = 10
        uploadSection2.props.margin_top = 10

        uploadSection3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 10)
        label_url = Gtk.Label("URL:...")
        uploadSection3.add(label_url)
        button_copy = Gtk.Button(label="Copy Url")
        button_copy.connect("clicked", self.CopyUrl)
        uploadSection3.add(button_copy)
        uploadSection3.props.margin_left = 10
        uploadSection3.props.margin_top = 10

        self.label_notfication = Gtk.Label("Click below to upload the screenshot")
        self.label_notfication.props.margin_left = 10
        self.label_notfication.props.width_chars = 32
        grid.attach(self.label_notfication, 2, 0, 2, 1)
        
        # attach the first upload section
        grid.attach(uploadSection1, 2, 1, 2, 2)

        self.grid = grid
        self.uploadSection1 = uploadSection1
        self.uploadSection2 = uploadSection2
        self.uploadSection3 = uploadSection3
        self.label_url = label_url

        config = ConfigWindow.LoadConfig()
        # if automatic upload then start uploading now
        if (config["automatic"]):
            self.Upload(None)

        # connect the main window to keypress
        self.connect("key-press-event", self.KeyPress)

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
        if (self.url):
            clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
            clipboard.set_text(self.url, -1)
            clipboard.store()

    def Upload(self, widget): 
        self.grid.remove(self.uploadSection1)
        self.grid.attach(self.uploadSection2, 2, 1, 2, 2)
        self.label_notfication.set_text("")
        self.grid.show_all()

        thread = Thread(target=self.StartUploading)
        thread.start()

    def StartUploading(self):
        uploader = ImgurUploader()
        result = uploader.Upload(self.filename)
        print(result)
        if (result['success']):
            self.label_url.set_markup("URL: <a href='" + result['link']+"'>" + result['link'] + "</a>")
            self.grid.remove(self.uploadSection2)
            self.grid.attach(self.uploadSection3, 2, 1, 2, 2)
            self.grid.show_all()
            self.url = result['link']
            self.label_notfication.set_text("Upload Successful !!")
        else:
            self.label_notfication.set_text("Upload Failed !! Try again !")
            self.grid.remove(self.uploadSection2)
            self.grid.attach(self.uploadSection1, 2, 1, 2, 2)
            self.grid.show_all()

    # for image saving
    def ImageSave(self, widget, pixbuf):
        dialog = Gtk.FileChooserDialog("Please choose a folder", self, Gtk.FileChooserAction.SAVE,
                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Save", Gtk.ResponseType.OK))

        filter_jpg = Gtk.FileFilter()
        filter_jpg.set_name("JPEG images")
        filter_jpg.add_pattern("*.jpg")
        dialog.add_filter(filter_jpg)
        dialog.set_default_size(50,50)
        dialog.set_do_overwrite_confirmation(True)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            print(dialog.get_filename())
            shot = Screenshot()
            shot.SaveShot(pixbuf, filename)
        dialog.destroy()

    def ImageCopy(self, widget, pixbuf):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_image(pixbuf)
        clipboard.store()

def main():
    GObject.threads_init()
    if platform.system() == 'Linux':
        Gdk.threads_init()

    win = ScreenEat()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()

    try:
        os.remove(win.filename)
    except:
        pass

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import platform, sys
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject
import ConfigWindow
from Screenshot import Screenshot
from threading import Thread
from ImgurUploader import ImgurUploader

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
            aspect = shot.active_height/shot.active_width
        else:
            pixel_buffer = shot.TakeShot(0,0, shot.full_width, shot.full_height, shot.root_window)
            aspect = shot.full_height/shot.full_width

        scaled = pixel_buffer.scale_simple(300,300*aspect, GdkPixbuf.InterpType.BILINEAR)
        image = Gtk.Image().new_from_pixbuf(scaled)
        grid.attach(image, 0, 0, 1, 4)

        # save shot for future
        shot.SaveShot(pixel_buffer, "test")


        box_buttons = Gtk.Box(spacing=10)
        box_buttons.props.margin_top = 10

        #button_save = Gtk.Button(label="Save To File")
        button_save = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_SAVE_AS))
        button_save.set_tooltip_text("save as")
        button_save.connect("clicked", self.ImageSave, pixel_buffer) #pixel buffer is passed
        box_buttons.add(button_save)

        #button_copy = Gtk.Button(label="Copy Image To Clipboard")
        button_copy = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_COPY))
        button_copy.set_tooltip_text("copy to clipboard")
        button_copy.connect("clicked", self.ImageCopy, pixel_buffer)
        box_buttons.add(button_copy)

        button_settings = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_PREFERENCES))
        button_settings.set_tooltip_text("settings")
        button_settings.connect("clicked", self.Configuration)
        box_buttons.add(button_settings)

        grid.attach(box_buttons, 0, 4, 3, 1)

        
        # create all 3 upload sections:

        uploadSection1 = Gtk.Box(spacing = 10)
        button_upload = Gtk.Button(label="Upload")
        button_upload.connect("clicked", self.Upload)
        uploadSection1.pack_start(button_upload, expand=True, fill=True, padding=0)
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
        if (config["Automatic"]):
            self.Upload(None)

        # connect the main window to keypress
        self.connect("key-press-event", self.KeyPress)

    def Configuration(self, widget):
        win = ConfigWindow.ConfigWindow()
        #win.connect("delete-event", Gtk.main_quit)
        win.show_all()
        #Gtk.main()

    def KeyPress(self, widget, event):
        # if Escape -> 65307 is the code
        if event.keyval==65307:
            Gtk.main_quit()
    
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
        result = uploader.Upload("test.jpg")
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
        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
                Gtk.FileChooserAction.SAVE,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                    "save", Gtk.ResponseType.OK))
        dialog.set_default_size(50,50)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            print(dialog.get_filename() + ".jpg")
            shot = Screenshot()
            shot.SaveShot(pixbuf, filename)
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
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


if __name__ == "__main__":
    main()

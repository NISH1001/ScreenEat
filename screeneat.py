import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from config import Config
from screen import Screen
from crop_window import CropWindow

class Handler:
    def __init__(self, builder):
        self.builder = builder

    def on_window_main_destroy(self, *args):
        Gtk.main_quit(*args)

    def on_upload_clicked(self, button):
        print("Upload")

    def on_copy_url_clicked(self, button):
        print("Copy Url")

    def on_save_to_disk_clicked(self, button):
        dialog = self.builder.get_object("filechooser_dialog")
        dialog.set_current_name(image.generate_filename())

        dialog.show_all()
        response = dialog.run()
        if response == 1:
            directory = os.path.dirname(dialog.get_filename())
            filename = os.path.basename(dialog.get_filename())
            image.digest(directory, filename)
        dialog.hide()

    def on_preferences_clicked(self, button):
        dialog = self.builder.get_object("preferences_dialog")

        dialog.show_all()
        response = dialog.run()
        if response == 1:
            pass
        dialog.hide()

    def on_copy_to_clipboard_clicked(self, button):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_image(image.pixbuf)
        clipboard.store()


builder = Gtk.Builder()
builder.add_from_file("screeneat.glade")
builder.connect_signals(Handler(builder))

# config = Config("~/ScreenEat/.config")
image = Screen().eat()
preview = image.copy()
preview.scale()

img = builder.get_object("screenshot_image")
img.set_from_pixbuf(preview.pixbuf)

window = builder.get_object("main_window")
window.show_all()

Gtk.main()

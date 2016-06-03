import os
import sys
import webbrowser

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from config import Config
from screen import Screen
from exception import AuthError
from crop_window import CropWindow
from imgur_public_uploader import ImgurPublicUploader
from imgur_private_uploader import ImgurPrivateUploader


def upload():
    #TODO: window hangs while working
    #TODO: not windows compatible
    filename = image.digest("/tmp")

    status = builder.get_object("status_label")
    status.set_text("Uploading")

    if config.data["authmode"] == "":
        status.set_text("Uploader not selected.")
        return
    elif config.data["authmode"] == 0:
        uploader = ImgurPublicUploader(publicauth)
        if not uploader.isConfigured():
            status.set_text("Uploader not configured.")
            return


        try:
            url = uploader.upload(filename)
        except AuthError as ae:
            status.set_text(ae.message)
            return
    elif config.data["authmode"] == 1:

        uploader = ImgurPrivateUploader(privateauth)
        if not uploader.isConfigured():
            status.set_text("Uploader not configured.")
            return

        access_pin = privateauth.data["access_pin"]
        if access_pin:
            try:
                uploader.getAccessToken(access_pin)
            except AuthError as ae:
                # Pin mismatch
                status.set_text(ae.message)
                return
            # need to get token from access pin for the first time only
            del privateauth.data["access_pin"]
            privateauth.save()
        else:
            if not uploader.isAuthenticated():
                status.set_text("Access Pin required.")
                return

        try:
            url = uploader.upload(filename)
        except AuthError as ae:
            # After access token is successfully retrived, AuthError
            # is generally caused by expired token
            uploader.renewAccessToken()
            #TODO: Error not caught for this code
            url = uploader.upload(filename)

        privateauth.save()

    status.set_text(url)
    # hide Upload button
    button = builder.get_object("upload_btn")
    button.set_sensitive(False)
    button.hide()
    # show CopyUrl button
    button = builder.get_object("copy_url_btn")
    button.set_sensitive(True)
    button.show()

    # Auto copy url
    if config.data["autocopy"]:
        copy_url()

def copy_url():
    status = builder.get_object("status_label")
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    clipboard.set_text(status.get_text(), -1)
    clipboard.store()

def copy_image():
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    clipboard.set_image(image.pixbuf)
    clipboard.store()

class Handler:
    def on_window_main_destroy(self, *args):
        Gtk.main_quit(*args)

    def on_upload_clicked(self, button):
        upload()

    def on_copy_url_clicked(self, button):
        copy_url()

    def on_copy_to_clipboard_clicked(self, button):
        copy_image()

    def on_private_open_browser_clicked(self, button):
        url = ImgurPrivateUploader.tokenUrl(privateauth.data["client_id"])
        webbrowser.open(url)

    def on_save_to_disk_clicked(self, button):
        dialog = builder.get_object("filechooser_dialog")
        dialog.set_current_name(image.generate_filename())

        dialog.show_all()
        response = dialog.run()
        if response == 1:
            directory = os.path.dirname(dialog.get_filename())
            filename = os.path.basename(dialog.get_filename())
            image.digest(directory, filename)
        dialog.hide()

    def on_preferences_clicked(self, button):
        dialog = builder.get_object("preferences_dialog")

        public_client_id = builder.get_object("public_client_id_text")
        public_client_id.set_text(publicauth.data["client_id"])

        private_client_id = builder.get_object("private_client_id_text")
        private_client_id.set_text(privateauth.data["client_id"])

        private_client_secret = builder.get_object("private_client_secret_text")
        private_client_secret.set_text(privateauth.data["client_secret"])

        private_access_pin = builder.get_object("private_access_pin_text")
        private_access_pin.set_text(privateauth.data["access_pin"])

        authmode_combo = builder.get_object("authmode_combo")
        authmode = config.data["authmode"]
        if authmode != "":
            authmode_combo.set_active(authmode)

        autocopy_check = builder.get_object("autocopy_check")
        autocopy_check.set_active(config.data["autocopy"])

        autoupload_check = builder.get_object("autoupload_check")
        autoupload_check.set_active(config.data["autoupload"])


        dialog.show_all()
        response = dialog.run()
        if response == 1:
            publicauth.data["client_id"] = public_client_id.get_text()
            publicauth.save()

            privateauth.data["client_id"] = private_client_id.get_text()
            privateauth.data["client_secret"] = private_client_secret.get_text()
            privateauth.data["access_pin"] = private_access_pin.get_text()
            privateauth.save()

            config.data["authmode"] = authmode_combo.get_active()
            config.data["autoupload"] = autoupload_check.get_active()
            config.data["autocopy"] = autocopy_check.get_active()
            config.save()

        dialog.hide()


arguments = sys.argv[1::]
if "--cropped" in arguments:
    image = Screen().eat()
    win = CropWindow(image)
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()

    if win.user_terminated:
        sys.exit(0)
    # After CropWindow exists, use the rectangle to crop the image.
    image.crop(win.rect.x, win.rect.y, win.rect.width, win.rect.height)

elif "--active" in arguments:
    image = Screen(active=True).eat()
else:
    image = Screen().eat()

preview = image.copy()
preview.scale()

privateauth_filename = "config/privateauth.json"
privateauth = Config(privateauth_filename)

publicauth_filename = "config/publicauth.json"
publicauth = Config(publicauth_filename)

config_filename = "config/config.json"
config = Config(config_filename)

glade_filename = "screeneat.glade"
builder = Gtk.Builder()
builder.add_from_file(glade_filename)

builder.connect_signals(Handler())

img = builder.get_object("screenshot_image")
img.set_from_pixbuf(preview.pixbuf)

window = builder.get_object("main_window")
window.show_all()

# Auto copy url
if config.data["autoupload"]:
    upload()

Gtk.main()

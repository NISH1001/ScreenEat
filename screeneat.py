#!/usr/bin/env python3

import os
import sys
import platform
import webbrowser
import signal

from threading import Thread
from time import sleep

import gi
gi.require_version('Gtk', '3.0')  # NOQA -- disable pep8 E402 warning
from gi.repository import Gtk, Gdk, GObject

from config import Config
from screen import Screen
from exception import AuthError, ManualError, Error
from crop_window import CropWindow
from imgur_public_uploader import ImgurPublicUploader
from imgur_private_uploader import ImgurPrivateUploader




def upload_worker():
    filename = image.digest(config_dir, ".tmp", config.data["quality"])
    upload_btn = builder.get_object("upload_btn")
    copy_url_btn = builder.get_object("copy_url_btn")
    status = builder.get_object("status_label")

    Gdk.threads_enter()
    status.set_text("Uploading...")
    upload_btn.set_sensitive(False)
    Gdk.threads_leave()

    try:
        # When authmode is not configured
        if config.data["authmode"] == "":
            raise ManualError("Uploader not selected.")

        # When public_imgur authmode is selected
        elif config.data["authmode"] == 0:
            uploader = ImgurPublicUploader(publicauth)
            if not uploader.isConfigured():
                raise ManualError("Imgur Public Uploader not configured.")
            # can raise AuthError
            url = uploader.upload(filename)

        # When private_imgur authmode is selected
        elif config.data["authmode"] == 1:

            uploader = ImgurPrivateUploader(privateauth)
            if not uploader.isConfigured():
                raise ManualError("Imgur Private Uploader not configured.")

            access_pin = privateauth.data["access_pin"]
            # If there is an access pin, then get new tokens from the pin
            if access_pin:
                # Pin mismatch Auth error
                uploader.getAccessToken(access_pin)
                # need to get token from access pin for the first time only
                del privateauth.data["access_pin"]
                privateauth.save()
            else:
                if not uploader.isAuthenticated():
                    raise ManualError("Access Pin required")
            # can raise AuthError
            url = uploader.upload(filename)
    except Error as e:
        Gdk.threads_enter()
        # DEBUG:
        print(e.message)
        status.set_text(e.message)
        upload_btn.set_sensitive(True)
        Gdk.threads_leave()
        return

    Gdk.threads_enter()
    # set status as url
    status.set_markup("<a href='" + url + "'>" + url + "</a>")
    # hide Upload button
    upload_btn.hide()
    upload_btn.set_sensitive(True)
    # show CopyUrl button
    copy_url_btn.show()
    copy_url_btn.set_sensitive(True)
    Gdk.threads_leave()

    # Auto copy url
    if config.data["autocopy"]:
        Gdk.threads_enter()
        copy_url(None)
        Gdk.threads_leave()


def upload_image(button):
    thread = Thread(target=upload_worker)
    thread.start()


def copy_url(button):
    status = builder.get_object("status_label")
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    clipboard.set_text(status.get_text(), -1)
    clipboard.store()


def copy_image(button):
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    clipboard.set_image(image.pixbuf)
    clipboard.store()


def open_browser(button):
    privateauth.data["client_id"] = private_client_id.get_text()
    url = ImgurPrivateUploader.tokenUrl(privateauth.data["client_id"])
    webbrowser.open(url)


def open_save_to_disk(button):
    dialog = builder.get_object("filechooser_dialog")
    dialog.set_current_name(image.generate_filename())

    dialog.show_all()
    response = dialog.run()
    if response == 1:
        directory = os.path.dirname(dialog.get_filename())
        filename = os.path.basename(dialog.get_filename())
        image.digest(directory, filename, config.data["quality"])
    dialog.hide()


def open_preferences(button):
    dialog = builder.get_object("preferences_dialog")

    public_client_id = builder.get_object("public_client_id_text")
    public_client_id.set_text(publicauth.data["client_id"])

    global private_client_id
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

    image_quality = builder.get_object("image_quality_text")
    image_quality.set_text(config.data["quality"])

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
        config.data["quality"] = image_quality.get_text()
        config.save()

    dialog.hide()


def on_key_press(window, event):
    keyval = event.keyval
    keyname = Gdk.keyval_name(keyval)

    # Handle escape to quit.
    if keyname == "Escape":
        Gtk.main_quit()

    ctrl = event.state & Gdk.ModifierType.CONTROL_MASK

    if ctrl:
        # Handle Ctrl+S to save.
        if keyname == "s":
            open_save_to_disk(None)
        # Handle Ctrl+C to copy.
        if keyname == "c":
            copy_image(None)


signal.signal(signal.SIGINT, signal.SIG_DFL)

argument = sys.argv[1] if len(sys.argv) > 1 else ""

config_dir = "~/.screeneat"
source_dir = os.path.dirname(os.path.realpath(__file__))

glade_filename = os.path.join(source_dir, "screeneat.glade")
privateauth_filename = os.path.join(config_dir, "privateauth.json")
publicauth_filename = os.path.join(config_dir, "publicauth.json")
config_filename = os.path.join(config_dir, "config.json")

# Load configuration files
privateauth = Config(privateauth_filename)
publicauth = Config(publicauth_filename, { "client_id": "9695b8de1e85072" })
config = Config(config_filename, { "authmode": 0, "autoupload": False, "autocopy": True, "quality": "98" })

# Get the Gui from glade file
builder = Gtk.Builder()
builder.add_from_file(glade_filename)

# Take a screenshot
image = Screen(active=(argument == "--active")).eat()

# Select snapshot mode
if argument == "--cropped":
    # Create a window to crop snaphost
    win = CropWindow(image)
    win.show_all()
    Gtk.main()
    # If user exited then no need to save the snapshot
    if win.user_terminated:
        sys.exit(0)
    # After CropWindow exists, use the rectangle to crop the image.
    image.crop(win.rect.x, win.rect.y, win.rect.width, win.rect.height)

# Initialize threads
GObject.threads_init()
if platform.system() == 'Linux':
    Gdk.threads_init()

# Set preview image from snapshot
preview = image.copy()
preview.scale(500)
screenshot_image = builder.get_object("screenshot_image")
screenshot_image.set_from_pixbuf(preview.pixbuf)

# Auto upload file
if config.data["autoupload"]:
    upload_image(None)

# Display the main window
main_window = builder.get_object("main_window")
main_window.show_all()

# Connect signals to widgets
handler = {
           "on_window_main_destroy": Gtk.main_quit,
           "on_key_press": on_key_press,
           "on_upload_clicked": upload_image,
           "on_copy_url_clicked": copy_url,
           "on_copy_to_clipboard_clicked": copy_image,
           "on_private_open_browser_clicked": open_browser,
           "on_save_to_disk_clicked": open_save_to_disk,
           "on_preferences_clicked": open_preferences
        }
builder.connect_signals(handler)

# Enter main loop
Gdk.threads_enter()
Gtk.main()
Gdk.threads_leave()

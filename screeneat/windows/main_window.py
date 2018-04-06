#!/usr/bin/env python3

import os
import sys
import webbrowser
from threading import Thread
from gi.repository import Gtk, Gdk

from screeneat.exception import ManualError, Error
from screeneat.uploaders.imgur_private_uploader import ImgurPrivateUploader
from screeneat.uploaders.imgur_public_uploader import ImgurPublicUploader
from screeneat.windows.screen import Screen
from screeneat.windows.crop_window import CropWindow


class MainWindow:
    def __init__(self, eat_active_screen, eat_cropped_screen,
                 temp_directory, config, privateauth, publicauth):

        # Configurations
        self.config = config
        self.privateauth = privateauth
        self.publicauth = publicauth
        self.temp_dir = temp_directory

        # Get the directory where the executable is located
        source_dir = os.path.dirname(os.path.realpath(__file__))
        self.glade_filename = os.path.join(source_dir, "main_window.glade")

        # Take image
        screen = Screen(active=eat_active_screen)
        self.image = screen.eat()

        # Open a window to crop image
        if eat_cropped_screen:
            crop_win = CropWindow(self.image)
            crop_win.show_all()

            # Enter main loop
            Gdk.threads_enter()
            Gtk.main()
            Gdk.threads_leave()

            # Handle termination gracefully
            if crop_win.user_terminated:
                sys.exit(0)

            # Crop the image
            crop_rect = crop_win.rect
            self.image.crop(crop_rect.x, crop_rect.y,
                            crop_rect.width, crop_rect.height)

        # Create preview image
        self.preview_image = self.image.copy().scale(500)

        self.url = ""

    def load(self):
        # Get the Gui from glade file
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.glade_filename)

        # Connect signals to widgets
        handler = {
                   "on_window_main_destroy": Gtk.main_quit,
                   "on_key_press": self.on_key_press,

                   "on_upload_clicked": self.upload_image,
                   "on_copy_url_clicked": self.copy_url,
                   "on_copy_to_clipboard_clicked": self.copy_image,

                   "on_private_open_browser_clicked": self.open_browser,
                   "on_save_to_disk_clicked": self.open_save_to_disk,
                   "on_preferences_clicked": self.open_preferences
                }
        self.builder.connect_signals(handler)

        # Load preview image in UI
        screenshot_image = self.builder.get_object("screenshot_image")
        screenshot_image.set_from_pixbuf(self.preview_image.pixbuf)

        # Display main window
        main_window = self.builder.get_object("main_window")
        main_window.show_all()

        # Auto upload file
        if self.config.data["autoupload"]:
            self.upload_image(None)

        # Enter main loop
        Gdk.threads_enter()
        Gtk.main()
        Gdk.threads_leave()

    def upload_worker(self):
        # Save image and get filename
        filename = self.image.digest(
            self.temp_dir,
            "screeneat",
            self.config.data["quality"])

        # Get UI elements
        upload_btn = self.builder.get_object("upload_btn")
        copy_url_btn = self.builder.get_object("copy_url_btn")
        status = self.builder.get_object("status_label")

        # Set uploading status
        Gdk.threads_enter()
        status.set_text("Uploading...")
        upload_btn.set_sensitive(False)
        Gdk.threads_leave()

        try:
            # When authmode is not configured
            if self.config.data["authmode"] == "":
                raise ManualError("Uploader not selected.")

            # When public_imgur authmode is selected
            elif self.config.data["authmode"] == 0:
                uploader = ImgurPublicUploader(self.publicauth)
                if not uploader.isConfigured():
                    raise ManualError("Imgur Public Uploader not configured.")
                # can raise AuthError
                self.url = uploader.upload(filename)

            # When private_imgur authmode is selected
            elif self.config.data["authmode"] == 1:

                uploader = ImgurPrivateUploader(self.privateauth)
                if not uploader.isConfigured():
                    raise ManualError("Imgur Private Uploader not configured.")

                access_pin = self.privateauth.data["access_pin"]
                # If there is an access pin, then get new tokens from the pin
                if access_pin:
                    # Pin mismatch Auth error
                    uploader.getAccessToken(access_pin)
                    # need to get token from access pin for the first time only
                    del self.privateauth.data["access_pin"]
                    self.privateauth.save()
                else:
                    if not uploader.isAuthenticated():
                        raise ManualError("Access Pin required")
                # can raise AuthError
                self.url = uploader.upload(filename)
        except Error as e:
            # DEBUG:
            print(e.message)

            # Show error, re-enable upload button
            Gdk.threads_enter()
            status.set_text(e.message)
            upload_btn.set_sensitive(True)
            Gdk.threads_leave()
            return

        Gdk.threads_enter()
        # Set status as url
        status.set_markup("<a href='" + self.url + "'>" + self.url + "</a>")
        # hide Upload button
        upload_btn.hide()
        upload_btn.set_sensitive(True)
        # show CopyUrl button
        copy_url_btn.show()
        copy_url_btn.set_sensitive(True)
        Gdk.threads_leave()

        # Auto copy url
        if self.config.data["autocopy"]:
            Gdk.threads_enter()
            self.copy_url(None)
            Gdk.threads_leave()

    def upload_image(self, button):
        thread = Thread(target=self.upload_worker)
        thread.start()

    def copy_url(self, button):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(self.url, -1)
        clipboard.store()

    def copy_image(self, button):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_image(self.image.pixbuf)
        clipboard.store()

    def open_browser(self, button):
        # Save client id before link is pressed (no need to save)
        private_client_id = self.builder.get_object("private_client_id_text")
        self.privateauth.data["client_id"] = private_client_id.get_text()

        # Get url and open in browser
        url = ImgurPrivateUploader.tokenUrl(self.privateauth.data["client_id"])
        webbrowser.open(url)

    def open_save_to_disk(self, button):
        dialog = self.builder.get_object("filechooser_dialog")
        dialog.set_current_name(self.image.generate_filename())

        dialog.show_all()
        response = dialog.run()
        if response == 1:
            directory = os.path.dirname(dialog.get_filename())
            filename = os.path.basename(dialog.get_filename())
            self.image.digest(directory, filename, self.config.data["quality"])
        dialog.hide()

    def open_preferences(self, button):
        dialog = self.builder.get_object("preferences_dialog")

        public_client_id = self.builder.get_object("public_client_id_text")
        public_client_id.set_text(self.publicauth.data["client_id"])

        private_client_id = self.builder.get_object("private_client_id_text")
        private_client_id.set_text(self.privateauth.data["client_id"])

        private_client_secret = self.builder.get_object(
                "private_client_secret_text")
        private_client_secret.set_text(self.privateauth.data["client_secret"])

        private_access_pin = self.builder.get_object("private_access_pin_text")
        private_access_pin.set_text(self.privateauth.data["access_pin"])

        authmode_combo = self.builder.get_object("authmode_combo")
        authmode = self.config.data["authmode"]
        if authmode != "":
            authmode_combo.set_active(authmode)

        autocopy_check = self.builder.get_object("autocopy_check")
        autocopy_check.set_active(self.config.data["autocopy"])

        autoupload_check = self.builder.get_object("autoupload_check")
        autoupload_check.set_active(self.config.data["autoupload"])

        image_quality = self.builder.get_object("image_quality_text")
        image_quality.set_text(self.config.data["quality"])

        dialog.show_all()
        response = dialog.run()
        if response == 1:
            self.publicauth.data["client_id"] = public_client_id.get_text()
            self.publicauth.save()

            self.privateauth.data["client_id"] = private_client_id.get_text()
            self.privateauth.data["client_secret"] = (
                private_client_secret.get_text()
            )
            self.privateauth.data["access_pin"] = private_access_pin.get_text()
            self.privateauth.save()

            self.config.data["authmode"] = authmode_combo.get_active()
            self.config.data["autoupload"] = autoupload_check.get_active()
            self.config.data["autocopy"] = autocopy_check.get_active()
            self.config.data["quality"] = image_quality.get_text()
            self.config.save()

        dialog.hide()

    def on_key_press(self, window, event):
        keyval = event.keyval
        keyname = Gdk.keyval_name(keyval)

        # Handle escape to quit.
        if keyname == "Escape":
            Gtk.main_quit()

        ctrl = event.state & Gdk.ModifierType.CONTROL_MASK

        if ctrl:
            # Handle Ctrl+S to save.
            if keyname == "s":
                self.open_save_to_disk(None)
            # Handle Ctrl+C to copy.
            if keyname == "c":
                self.copy_image(None)

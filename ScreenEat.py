from gi.repository import Gtk, Gdk, GdkPixbuf
import ConfigWindow
from Screenshot import Screenshot

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

        # span : from col=0, row=0, to col=1, row=4
        imageprev= Gtk.Label("imagepreview")
        pixel_buffer = GdkPixbuf.Pixbuf.new_from_file("test.jpg")
        scaled = pixel_buffer.scale_simple(200,150, GdkPixbuf.InterpType.BILINEAR)
        image = Gtk.Image().new_from_pixbuf(scaled)
        grid.attach(image, 0, 0, 1, 4)

        button_save = Gtk.Button(label="Save To File")
        button_save.props.margin_left = 10
        button_save.connect("clicked", self.ImageSave, pixel_buffer) #pixel buffer is passed
        grid.attach(button_save, 2, 0, 1, 1)

        button_copy = Gtk.Button(label="Copy Image To Clipboard")
        button_copy.props.margin_left = 10
        #button_copy.set_sensitive(False)
        button_copy.connect("clicked", self.ImageCopy, pixel_buffer)
        grid.attach(button_copy, 3, 0, 1, 1)

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

    def ImageCopy(self, widget, pixbuf):
        clipboard = Gtk.Clipboard()
        clipboard.set_image(pixbuf)
        clipboard.store()


def main():
    win = ScreenEat()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()

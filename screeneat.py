import argparse
import os
import platform
import signal
import tempfile
import gi
gi.require_version('Gtk', '3.0')  # NOQA -- disable pep8 E402 warning
gi.require_version('Gdk', '3.0')  # NOQA -- disable pep8 E402 warning
from gi.repository import Gdk, GObject

from screeneat.config import Config
from screeneat.windows.main_window import MainWindow


def parse():
    HOME = os.expanduser("~")
    config_path = os.join(HOME, '.screeneat.conf')

    parser = argparse.ArgumentParser(
        "screeneat",
        description="screenshot made delicious "
    )

    optype = parser.add_mutually_exclusive_group()

    optype.add_argument('-a',
                        '--active',
                        dest='eat_active_screen',
                        help='Screenshot active region',
                        action='store_const',
                        const=True)

    optype.add_argument('-c',
                        '--cropped',
                        dest='eat_cropped_screen',
                        help='Screenshot cropped region',
                        action='store_const',
                        const=True)

    parser.add_argument('-C',
                        '--config',
                        dest='config_path',
                        help='Path to configuration file',
                        metavar='configuration file',
                        type=str,
                        default=config_path,
                        required=False)

    return parser.parse_args()


def main():
    args = parse()

    # Register OS signals
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Initialize threads for Gdk
    GObject.threads_init()
    if platform.system() == 'Linux':
        Gdk.threads_init()

    # Load configurations
    privateauth_filename = os.join(args.config_path, "privateauth.json")
    publicauth_filename = os.join(args.config_path, "publicauth.json")
    config_filename = os.join(args.config_path, "config.json")

    # Load all configuration files
    privateauth_config = Config(privateauth_filename)
    publicauth_config = Config(
        publicauth_filename,
        {"client_id": "9695b8de1e85072"}
    )
    screeneat_config = Config(
        config_filename,
        {
            "authmode": 0,
            "autoupload": False,
            "autocopy": True,
            "quality": "98"
        }
    )

    temp_dir = tempfile.gettempdir()

    main = MainWindow(
        args.eat_active_screen,
        args.eat_cropped_screen,
        temp_dir,
        screeneat_config,
        privateauth_config,
        publicauth_config,
    )
    main.load()


if __name__ == "__main__":
    main()

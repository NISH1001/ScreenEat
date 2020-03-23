# ScreenEat #

Screenshots made delicious and easy.

1. Take a screenshot.
2. Upload screenshot to an online account.
3. Get a shareable *url* of your screenshot.

![ScreenEat Screenshot](https://user-images.githubusercontent.com/4928045/30070550-7ddf1f3e-9283-11e7-86f7-2fd846916474.jpeg)

Say goodbye to the old and cumbersome method of taking a screenshot,  saving it on disk, uploading it and finally sharing the link.

## Usage ##

ScreenEat allows you to take screenshot of the whole screen,  the active window or a cropped region of the screen.

```bash
# Whole Screen
screen-eat

# Active Window
screen-eat --active

# Cropped Screen
screen-eat --cropped
```

You may want to bind keyboard shortcuts to these commands, the process to do which depends on the system you are using.

## Ok! I want to it, but how? ##

Checkout the latest sources with:

```bash
git clone https://github.com/NISH1001/ScreenEat.git
```

ScreenEat requires **Python3** and **PyGObject** to be installed. Also make sure you have Gtk+ version >= 3.10.

```bash
# Get dependencies for debian
apt install python3 python3-gi

# Get dependencies for archlinux
pacman -S python-gobject python-cairo
```

## Installation with setup.py

## Installation with pip ##

It's as easy as

```bash
pip3 install screen-eat
```

If you cannot find the package in pip, you can use setup.py

```bash
python setup.py install --user
```

## For i3 window manager ##

Add the following to your i3 config:

```
# Bindings to take screenshot
bindsym Print exec screen-eat
bindsym Shift+Print exec screen-eat --active
bindsym --release $mod+Print exec screen-eat --cropped

# Bindings with to take screenshot after 2 seconds
bindsym Ctrl+Print exec sleep 2 && screen-eat
bindsym Ctrl+Shift+Print exec sleep 2 && screen-eat --active
bindsym --release Ctrl+$mod+Print exec sleep 2 && screen-eat --cropped
```

## ScreenEat with Imgur ##

Before you can start uploading screenshots using ScreenEat, you will first need an *imgur* account. You can still take screenshots and save it locally on your disk.

1. Create an [imgur](https://imgur.com/) account.
2. Register an application from https://api.imgur.com/oauth2/addclient.
3. Go to *Preferences* and enter the authorization details.

### Fields required for application registration ###

Field                       | Detail
--------------------------- | ------------------
Application name            | ScreenEat
Authorization type          | ...
Authorization callback URL  | *Optional*
Website                     | *Optional*
Email                       | Your email address
Description                 | *Optional*

You can choose the *Authorization type* that best suits you.

Authorization type                          | What does it mean for you?
------------------------------------------- | ------------------------------------
OAuth2 authorization with a callback URL    | Upload private snapshots and requires an authorization callback URL.
OAuth2 authorization without callback URL   | Upload private snapshots.
Anonymous user without user authorization   | Upload public snapshots anonymously.
---


## Contributing to this project ##

ScreenEat is open-source and you can contribute to it if you like.

If you are a developer and find a bug, and has fixes for the problem as well, you may send us a pull request any time.

If want to **contribute**, make sure you first read [CONTRIBUTING.md](https://github.com/NISH1001/ScreenEat/blob/master/CONTRIBUTING.md).


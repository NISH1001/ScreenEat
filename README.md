# ScreenEat #

Screenshots made delicious and easy. 

1. Take a screenshot.
2. Upload screenshot to an online account.
3. Get a shareable *url* of your screenshot.

![ScreenEat Screenshot](https://cloud.githubusercontent.com/assets/4928045/18194070/c490653a-7102-11e6-86fa-23b08f63aa13.png)

Say goodbye to the old and cumbersome method of taking a screenshot,  saving it on disk, uploading it and finally sharing the link.

## Usage ##

ScreenEat allows you to take screenshot of the whole screen,  the active window or a cropped region of the screen.

```bash
# Whole Screen
./screeneat.py

# Active Window
./screeneat.py --active

# Cropped Screen
./screeneat.py --cropped
```

You may want to bind keyboard shortcuts to these commands, the process to do which depends on the system you are using.

### For i3 window manager ###

Add these to your i3 config, Change *DIR* to the location of ScreenEat:

    bindsym Print exec DIR/python3 screeneat.py
    bindsym Shift+Print exec python3 DIR/screeneat.py --active
    bindsym --release $mod+Print exec python3 DIR/screeneat.py --cropped

## Ok! I want to it, but how? ##

Checkout the latest sources with:

    git clone https://github.com/NISH1001/ScreenEat.git

ScreenEat requires **Python3** and **PyGObject** to be installed. Also make sure you have Gtk+ version >= 3.10.

    # Get dependencies for debian
    sudo apt-get install python3 python3-gi

## ScreenEat with Imgur ##

Before you can start uploading screenshots using ScreenEat, you will first need an *imgur* account. You can still take screenshots and save it locally on your disk.

1. Create an [imgur](https://imgur.com/) account.
2. Register an application from https://api.imgur.com/oauth2/addclient.
3. Go to *Preferences* and enter the authorization details.

### Fields required for application registration ###

Field                       | Detail
--------------------------- | ------------------
Application name            | ScreenEat
Authorization callback URL  | *Blank*
Website                     | *Optional*
Email                       | Your email address
Description                 | *Optional*
Authorization type          | ...

You can choose the *Authorization type* that best suits you.

Authorization type                          | What does it mean for you?
------------------------------------------- | ------------------------------------
OAuth2 authorization without callback       | Upload private snapshots.
Anonymous user without user authorization   | Upload public snapshots anonymously.
 
---


## Contributing to this project ##

ScreenEat is open-source and you can contribute to it if you like.

If you are a developer and find a bug, and has fixes for the problem as well, you may send us a pull request any time.

If want to **contribute**, make sure you first read [CONTRIBUTING.md](https://github.com/NISH1001/ScreenEat/blob/master/CONTRIBUTING.md).


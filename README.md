# ScreenEat #

Screenshots made delicious and easy.

## What is it? ##

ScreenEat is a free and simple tool that makes sharing desktop snapshots easy and simple. It provides a way to capture screenshots of any part of your desktop, allows you to instantly upload it to your account and gives your a shareable *url* which links to the uploaded image.

This removes the old cumbersome method of first capturing screenshot, then saving it, then uploading it and finally sharing the link  and instead provides a one-step solution making sharing job faster and teamworks efficient.


## Ok! I want to use it, but how? ##

Checkout the latest source code:

    git clone https://github.com/NISH1001/ScreenEat.git

ScreenEat requires **Python3** and **PyGObject** to be installed. Get the dependencies for debian systems using:

    sudo apt-get install python3 python3-gi

Also make sure you have Gtk+ >= 3.10.

ScreenEat allows you to take screenshot of the whole screen, only the active window or a cropped part of the screen.

```bash
# Whole screenshot
./screeneat.py

# Active window screenshot:
./screeneat.py --active

# Crop mode screenshot:
./screeneat.py --cropped
```

You may want to bind keyboard shortcuts to these commands, the process to do which depends on the system you are using.

### ScreenEat with Imgur ###

Before you can start uploading snapshots using ScreenEat, you will first need an [imgur](https://imgur.com/) account.

1. Create an imgur account.
2. Register an application from https://api.imgur.com/oauth2/addclient.

Enter the following details for registration.

Field                       | Detail
--------------------------- | ------------------
Application name            | ScreenEat
Authorization callback URL  | *Blank*
Website                     | *Optional*
Email                       | your email address
Description                 | *Optional*

Choose the Authorization type that best suits your application.

Authorization type                          | Detail
------------------------------------------- | ------------------------------------
OAuth2 authorization without callback       | Upload private snapshots.
Anonymous user without user authorization   | Upload public snapshots anonymously.

---


## Contributing to this project ##

ScreenEat is open-source and you can contribute to it if you like.

If you are a developer and find a bug, and has fixes for the problem as well, you may send us a pull request any time.

If want to **contribute**, make sure you first read [CONTRIBUTING.md](https://github.com/NISH1001/ScreenEat/blob/master/CONTRIBUTING.md).

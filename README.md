# ScreenEat #

Screenshots made delicious and easy.

## What is it? ##

ScreenEat is a free and simple tool to make sharing desktop screenshots sure easy. It provides a shareable *url* after uploading the screenshot to the web.

## Why use it? ##

Reason is simple : *no local storage - immediate sharing*

Forget the old time-taking process of:

1. Pressing `PrintScr`.
2. Saving the screenshot to a local file.
3. Uploading the file so that you may share it.

Instead, the process simplifies into **pressing a key**.

## Ok! I want to use it, but how? ##

Checkout the latest sources:

    git clone https://github.com/NISH1001/ScreenEat.git

ScreenEat requires **Python3** and **PyGObject** to be installed. Get the dependencies for debian systems using:

    sudo apt-get install python3 python3-gi

ScreenEat allows you to take screenshot of the whole screen, active window and the cropped window.

```bash
# Whole screenshot
./screeneat.py

# Active window screenshot:
./screeneat.py --active

# Cropped window screenshot:
./screeneat.py --cropped
```

### ScreenEat with Imgur ###

Before you can start uploading snapshots using ScreenEat, you would first need an imgur account.

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

## Related Links ##

Find more about this project at:

- [http://code-momo.herokuapp.com/blog/post/screeneat-delicious-screenshots](http://code-momo.herokuapp.com/blog/post/screeneat-delicious-screenshots/)
- [http://codingparadox.herokuapp.com/blog/detail/screeneat-delicious-screenshots](http://codingparadox.herokuapp.com/blog/detail/screeneat-delicious-screenshots)

## Contributing to this project ##
ScreenEat is open-source and you can contribute too if you like.  
If want to **contribute**, make sure you first read [CONTRIBUTING.md](https://github.com/NISH1001/ScreenEat/blob/master/CONTRIBUTING.md)

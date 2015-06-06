# ScreenEat

## What the heck is it?

It is a simple tool to make sharing your desktop screenshots super easy.
It offers you to share the screenshot by immediately uploading the snap to web and gives you an immediate sharable *url*.

> Currently, ScreenEat uses [**Imgur**](http://imgur.com/) to store the uploaded images, as it seems the most convenient option for now. This can change in future if problems arise.

## Why use it?

Reason is simple : *no local storage - immediate share*

Forget the old time-wasting process of :

1. Hitting `PrintScr`
2. Saving screenshot to a local file
3. Finally, uploading the file so that you may share it

Instead the process is simplified to **just hitting the default keybinding to take screenshot with our app**.

- If *automatic upload* is enabled, a sharable *url* is provided immediately
- If *automatic upload* is disabled, you can click the upload button and a sharable *url* is then provided

You still get options to *save* a local copy and *copy* the screenshot image to clipboard.

## Ok! I want to use it, but how?

#### Clone this repo first

```bash
git clone https://github.com/NISH1001/ScreenEat.git
```

#### Our default key binding

Insize the newly created *ScreenEat* folder, run the `keybindings.py` script as :

```bash
./keybindings.py
```
Once done, following keybindings are set:
* `ctrl+super+p` : Take screenshot of the whole desktop
* `ctrl+super+o` : Take screenshot of only the active window






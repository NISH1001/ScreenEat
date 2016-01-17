# ScreenEat

Screenshots made delicious and easy.

## What is it?

It is a simple open- source tool to make sharing your desktop screenshots super easy.
It offers you to share the screenshot by immediately uploading the snap to web and gives you a sharable *url*.

> Currently, ScreenEat uses [**Imgur**](http://imgur.com/) to store the uploaded images, as it seems the most convenient option for now. This can change in future if needed.

## Why use it?

Reason is simple : *no local storage - immediate sharing*

Forget the old time-taking process of :

1. Hitting `PrintScr`
2. Saving screenshot to a local file
3. Finally, uploading the file so that you may share it

Instead the process is simplified to **just hitting the default keybinding to take screenshot with our application**.

- If *automatic upload* is enabled, a sharable *url* is provided immediately
- If *automatic upload* is disabled, you can click the upload button and a sharable *url* is then provided

You still get options to *save* a local copy and *copy* the screenshot image to clipboard.

## Ok! I want to use it, but how?

#### Clone this repo first

```bash
git clone https://github.com/NISH1001/ScreenEat.git
```

> You need **Python3** and **PyGObject** installed to use ScreenEat. For debian systems, these can be installed using following bash command lines respectively:

```bash
sudo apt-get install python3
sudo apt-get install python3-gi
```

#### Our default key binding

Inside the newly created *ScreenEat* folder, run the `keybindings.py` script once as :

```bash
./keybindings.py
```
Once done, following keybindings are set:

- **`Ctrl+Super+P`** : Take screenshot of the whole desktop
- **`Ctrl+Super+O`** : Take screenshot of only the active window
- **`Ctrl+Super+I`** : Take cropped screenshot of the whole window

> There is no need to run this script again. The keybindings are set and can be changed from `System Settings > Keyboard > Shortcuts > Custom Shortcuts` in Ubuntu.

### Command lines to run ScreenEat

Well, there are keybindings so you are less likely to use it. Still here's the examples of command lines to run ScreenEat through terminal.

Full screen snapshot:

```bash
./ScreenEat.py
```

Active window snapshot:

```bash
./ScreenEat.py --active
```

Cropped window snapshot:

```bash
./ScreenEat.py --cropped
```

### Configurations

The settings are stored in `config.json` file and can be changed manually or through the settings dialog box.

##### Options available

`automatic-upload` : Set whether to automatically upload image immediately after taking the screenshot

`automatic-copy-url` : Set whether to automatically copy url after uploading is completed

----

### Related Links

Find more about this project at:

- [http://code-momo.herokuapp.com/blog/post/screeneat-delicious-screenshots](http://code-momo.herokuapp.com/blog/post/screeneat-delicious-screenshots/)
- [http://codingparadox.herokuapp.com/blog/detail/screeneat-delicious-screenshots](http://codingparadox.herokuapp.com/blog/detail/screeneat-delicious-screenshots)

### Contributing to this project
ScreenEat is open-source and you can contribute too if you like.  
If want to **contribute**, make sure you first read [CONTRIBUTING.md](https://github.com/NISH1001/ScreenEat/blob/master/CONTRIBUTING.md)

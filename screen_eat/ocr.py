#!/usr/bin/env python3

import sys
from PIL import Image
import pytesseract


def image_to_text(img):
    try:
        return pytesseract.image_to_string(img)
    except:
        return ""


def main():
    path = sys.argv[1]
    text = pytesseract.image_to_string(Image.open(path))
    print(text)


if __name__ == "__main__":
    main()

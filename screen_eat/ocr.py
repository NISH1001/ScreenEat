#!/usr/bin/env python3

import sys

import cv2
import numpy as np
from PIL import Image
import pytesseract

try:
    import easyocr

    EASYOCR = True
except:
    EASYOCR = False


def resize_image(img, width=None, height=None):
    h, w = img.shape[:2]
    aspect_ratio = w / h
    if not height:
        height = int(width / aspect_ratio)
    if not width:
        width = int(height * aspect_ratio)
    return cv2.resize(img, (width, height), cv2.INTER_CUBIC)


def load_image(img, target_size=(), filename=None):
    """
        This is a mega image loader.

        img: str or PIL

        target_size (width, height):
            - if both None, no resizing is done
            - if one of the values is given, resizing is done keeping the
            aspect ratio same

        filename: str
            If provided, the image will also be saved in this location
    """
    if type(img) is str:
        img = cv2.imread(img)
    elif "PIL" in str(type(img)):
        img = np.array(img)
    if target_size and len(target_size) == 2:
        if all(target_size):
            img = cv2.resize(img, target_size)
        if target_size[0] is not None and target_size[1] is None:
            img = resize_image(img, width=target_size[0], height=None)
        if target_size[0] is None and target_size[1] is not None:
            img = resize_image(img, width=None, height=target_size[1])
    if filename:
        cv2.imwrite(filename, img)
    return img


def _use_pytesseract(img):
    print("Using pytesseract...")
    try:
        return pytesseract.image_to_string(img)
    except Exceptionas as e:
        print(str(e))
        return ""


def _use_easyocr(img):
    print("Using easyocr...")
    try:
        img = load_image(img)
        reader = easyocr.Reader(["en"], gpu=False, download_enabled=False)
        result = reader.readtext(img, detail=0)
        return "\n".join(result)
    except Exception as e:
        print(str(e))
        return ""


def image_to_text(img, mode="pytesseract"):
    func = _use_pytesseract
    if mode == "easyocr" and EASYOCR:
        func = _use_easyocr
    if mode == "easyocr" and not EASYOCR:
        func = _use_pytesseract
    text = func(img)
    print(f"OCRed Text = {text}")
    return text


def main():
    path = sys.argv[1]
    text = image_to_text(Image.open(path), mode="easyocr")
    print(text)


if __name__ == "__main__":
    main()

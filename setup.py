#!/bin/python3

from distutils.core import setup

setup(
    name='ScreenEat',
    version='1.0',
    description='Screen Capturing Made Delicious',
    author='Nishan Pantha, Bibek Dahal, Safar Ligal, Bibek Pandey',
    author_email='bewakepandey@gmail.com',
    packages=['screeneat', 'screeneat.windows', 'screeneat.uploaders'],
    scripts=['screen-eat']
)

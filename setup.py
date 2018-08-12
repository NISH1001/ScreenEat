#!/bin/python3

from distutils.core import setup

setup(
    name='ScreenEat',
    version='1.0',
    description='Screen Capturing Made Delicious',
    author='Nishan Pantha, Bibek Dahal, Safar Ligal, Bibek Pandey',
    author_email='nishanpantha@gmail.com, bibek.dahal@togglecorp.com, weathermist@gmail.com, bewakepandey@gmail.com',  # noqa
    packages=['screen_eat', 'screen_eat.windows', 'screen_eat.uploaders'],
    package_data={
        '': ['*.glade']
    },
    scripts=['screen-eat']
)

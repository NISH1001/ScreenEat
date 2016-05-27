# ScreenEat #
Screenshots made delicious and easy.

## Authenticating with Imgur ##

Go to https://api.imgur.com/oauth2/addclient and register an application with the
following details, so that you can start uploading your snapshots using ScreenEat.

Field                       | Data
--------------------------- | -------------------------------------------------------------------------------------
Application name            | ScreenEat
Authorization type          | OAuth 2 authorization without callback <br> Anonymous user without user authorization
Authorization callback URL  | *Blank*
Website                     | *Optional*
Email                       | your email address
Description                 | *Optional*


Authorization type                          | Details
------------------------------------------- | -------------------------------------------------
OAuth2 authorization without callback       | It allows uploading private snapshots.
Anonymous user without user authorization   | It allows uploading public snapshots anonymously.

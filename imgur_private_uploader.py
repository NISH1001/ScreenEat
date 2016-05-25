import webbrowser
import requests
import pprint
from uploader import Uploader
from exception import AuthError
from config import Config


class ImgurPrivateUploader(Uploader):
    """An uploader to upload public image to imgur anonymously."""

    def __init__(self, auth):
        self.auth = auth

    def url(self):
        return "https://api.imgur.com/3/upload"

    def headers(self):
        return {"authorization":
                "Bearer {0}".format(self.auth.data["access_token"])}

    def isAuthenticated(self):
        return (self.auth.data["access_token"]!="" and
                self.auth.data["refresh_token"]!="")

    def tokenUrl(self):
        url = ("https://api.imgur.com/oauth2/authorize?"+
               "client_id={client_id}&response_type=pin&state=anything")
        return url.format(client_id=self.auth.data["client_id"])

    def getAccessToken(self, pin):
        url = "https://api.imgur.com/oauth2/token/"
        payload = {"client_id" : self.auth.data["client_id"],
                   "client_secret" : self.auth.data["client_secret"],
                   "pin": pin,
                   "grant_type" : "pin"}

        rj = self.request(url, payload)
        self.auth.data["access_token"] = rj['access_token']
        self.auth.data["refresh_token"] = rj['refresh_token']

    def renewAccessToken(self):
        url = r"https://api.imgur.com/oauth2/token/"
        payload = {"client_id" : self.auth.data["client_id"],
                   "client_secret" : self.auth.data["client_secret"],
                   "refresh_token": self.auth.data["refresh_token"],
                   "grant_type" : "refresh_token"}

        rj = self.request(url, payload)
        self.auth.data["access_token"] = rj['access_token']
        self.auth.data["refresh_token"] = rj['refresh_token']


if __name__ == "__main__":
    filename = "data/panda.jpg"
    authfile = "~/ScreenEat/data/privateauth.json"

    auth = Config(authfile)
    # if there is no previous data about client
    if not auth.data["client_id"]:
        client_id = input("Enter the client id: ")
        client_secret = input("Enter the client secret: ")
        auth.data["client_id"] = client_id
        auth.data["client_secret"] = client_secret

    imguru = ImgurPrivateUploader(auth)

    # Check for client_id and client_secret mismatch

    # This is done once
    if not imguru.isAuthenticated():
        url = imguru.tokenUrl()
        webbrowser.open(url)
        # Try until correct pin is entered
        while True:
            try:
                pin = input("Enter the access pin: ")
                imguru.getAccessToken(pin)
                # If eveything okay, then break from the eternal loop
                break
            except AuthError as ae:
                # Pin mismatch
                print(ae)
    auth.save()

    try:
        print(imguru.upload(filename))
    except AuthError as ae:
        # Access Token expired or invalid
        print(ae)
        imguru.renewAccessToken()
        print(imguru.upload(filename))

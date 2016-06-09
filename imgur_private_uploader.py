import webbrowser
import pprint
from uploader import Uploader
from config import Config
from exception import AuthError


class ImgurPrivateUploader(Uploader):
    """An uploader to upload public image to imgur anonymously."""

    def __init__(self, auth):
        self.auth = auth

    def url(self):
        return "https://api.imgur.com/3/upload"

    def headers(self):
        return {"authorization":
                "Bearer {0}".format(self.auth.data["access_token"])}

    def isConfigured(self):
        return (self.auth.data["client_id"] != "" and
                self.auth.data["client_secret"] != "")

    def isAuthenticated(self):
        return (self.auth.data["access_token"] != "" and
                self.auth.data["refresh_token"] != "")

    @staticmethod
    def tokenUrl(client_id):
        url = ("https://api.imgur.com/oauth2/authorize?" +
               "client_id={id}&response_type=pin&state=anything")
        return url.format(id=client_id)

    def getAccessToken(self, pin):
        url = "https://api.imgur.com/oauth2/token/"
        payload = {"client_id": self.auth.data["client_id"],
                   "client_secret": self.auth.data["client_secret"],
                   "pin": pin,
                   "grant_type": "pin"}

        rj = self.request(url, payload)
        self.auth.data["access_token"] = rj['access_token']
        self.auth.data["refresh_token"] = rj['refresh_token']

    def renewAccessToken(self):
        url = r"https://api.imgur.com/oauth2/token/"
        payload = {"client_id": self.auth.data["client_id"],
                   "client_secret": self.auth.data["client_secret"],
                   "refresh_token": self.auth.data["refresh_token"],
                   "grant_type": "refresh_token"}

        rj = self.request(url, payload)
        self.auth.data["access_token"] = rj['access_token']
        self.auth.data["refresh_token"] = rj['refresh_token']

    def upload(self, filename):

        try:
            url = Uploader.upload(self, filename)
        except AuthError as ae:
            # After access token is successfully retrived,
            # AuthError is generally caused by expired token
            # TODO: Getting timestamp or reading json file for exact error
            renewAccessToken()
            # Try to upload once again
            url = Uploader.upload(self, filename)
            # Save any changes by renewAccessToken
            self.auth.save()

        return url

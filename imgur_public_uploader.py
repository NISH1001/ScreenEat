from config import Config
from uploader import Uploader


class ImgurPublicUploader(Uploader):
    """An uploader to upload public image to imgur anonymously."""

    def __init__(self, auth):
        self.auth = auth

    def url(self):
        return "https://api.imgur.com/3/image"

    def headers(self):
        return {"Authorization":
                "Client-ID {0}".format(self.auth.data["client_id"])}


if __name__ == "__main__":
    filename = "data/panda.jpg"
    authfile = "~/ScreenEat/data/publicauth.json"

    auth = Config(authfile)
    # if there is no previous data about client
    if not auth.data["client_id"]:
        client_id = input("Enter the client id: ")
        auth.data["client_id"] = client_id

    imguru = ImgurPublicUploader(auth)
    print(imguru.upload(filename))
    auth.save()

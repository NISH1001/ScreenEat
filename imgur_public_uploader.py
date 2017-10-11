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

    def isConfigured(self):
        return self.auth.data["client_id"] != ""

import requests
import base64
from abc import ABCMeta
from abc import abstractmethod
from exception import AuthError, ManualError


class Uploader(metaclass=ABCMeta):
    """An uploader class."""

    # Uploader specific target url
    @abstractmethod
    def url(self):
        pass

    # Uploader specific header
    @abstractmethod
    def headers(self):
        pass

    def payload(self, filename):
        return {'image': base64.b64encode(open(filename, 'rb').read()),
                'name': filename,
                'type': 'base64',
                'title': 'ScreenEat Upload'}

    # Post request with payload and headers
    def request(self, url, payload, headers=None):
        try:
            # make the upload, ensuring that the data, headers are included
            if headers:
                r = requests.post(url, data=payload, headers=headers,
                                  verify=True)
            else:
                r = requests.post(url, data=payload, verify=True)
        except Exception:
            # TODO: better exception handling
            raise ManualError("Error in connection.")

        # save the json response
        rj = r.json()
        # check for success
        if "success" in rj and not rj["success"]:
            raise AuthError(rj["status"], rj["data"]["error"])
        return rj

    def upload(self, filename):
        """Upload image given the filename in disk."""

        rj = self.request(self.url(), self.payload(filename), self.headers())
        return rj["data"]["link"]

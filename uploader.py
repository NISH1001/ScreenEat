import requests
import base64
from abc import ABCMeta
from abc import abstractmethod
from exception import AuthError


class Uploader(metaclass=ABCMeta):
    """An uploader class."""

    @abstractmethod
    def url(self):
        pass

    @abstractmethod
    def headers(self):
        pass

    def payload(self, filename):
        return {'image' : base64.b64encode(open(filename, 'rb').read()),
                'name' : filename,
                'type':'base64',
                'title':'ScreenEat Upload'}

    def request(self, url, payload, headers=None):
        # make the upload, ensuring that the data, headers are included
        if headers:
            r = requests.post(url, data=payload, headers=headers, verify=True)
        else:
            r = requests.post(url, data=payload, verify=True)
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
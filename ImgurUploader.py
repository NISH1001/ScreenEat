#!/usr/bin/env python3
import base64, requests, datetime

"""
An uploader class to upload image to imgur
Upload : Method to upload a file to imgur
"""
class ImgurUploader():
    def __init__(self):
        client_id = "e8ac1a4090ab0b3"
        self.headers = {"Authorization": "Client-ID "+client_id}


    def Upload(self, filename):
        try:
            # upload route
            url = "https://api.imgur.com/3/image"
            
            # record time for debug purposes
            prev_time = datetime.datetime.now()

            # POST with file data encoded in base64
            response = requests.post(
                url,
                headers=self.headers,
                data = {
                    'image': base64.b64encode(open(filename, 'rb').read()),
                    'type': 'base64',
                    'name': filename,
                    'title': 'ScreenEat Upload'
                }
            )

            response_json = response.json()

            delta_time = datetime.datetime.now()-prev_time

            # return result
            result = {}
            result["success"] = response_json["success"]
            result["time-in-seconds"] = delta_time.total_seconds()
            if (result["success"]):
                result["link"] = response_json["data"]["link"]
            return result
        except:
            return {'success': False}
        

def main():
    imguru = ImgurUploader()
    print("Uploading")
    result = imguru.Upload("test.jpg")
    print(result)


if __name__=="__main__":
    main()

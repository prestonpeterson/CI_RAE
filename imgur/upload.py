#!/usr/bin/env python3

# \author Mattias Huber, Preston Peterson, Phillip Porter, Heather Bradfield, Zoltan Batoczki, Jesus Bamford
# \copyright GNU Public License.

"""@package docstring
This package handles image uploads to imgur
"""

from imgur.imgur_settings import client_id, client_secret
from imgurpython import ImgurClient
imgur_client = ImgurClient(client_id, client_secret)

def upload_image(image_path):
    """
    :param client: the relative path to the image to be uploaded. e.g. 'test.png'
    :return: string URL of the uploaded image.
             or return "UPLOAD_ERROR" if an exception occurs, such as the imgur servers being busy.
    """
    print("Uploading image... ")
    try:
        image = imgur_client.upload_from_path(image_path, config=None, anon=True)
    except Exception as e:
        print('Error uploading image: ', e)
        return "UPLOAD_ERROR"
    print("Done uploading")
    return format(image['link'])

#!/usr/bin/env python3

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


# The following is for testing of imgur uploads
if __name__ == "__main__":
    image_path = 'test.png'
    image_url = upload_image(image_path)
    print("Image posted. Here is the link: ", image_url)
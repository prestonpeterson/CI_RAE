#!/usr/bin/env python3


def upload_image(imgur_client, image_path):
    """
    :param client: the path to the image to be uploaded. e.g.
    :return: string URL of the uploaded image
    """
    print("Uploading image... ")
    try:
        image = imgur_client.upload_from_path(image_path, config=None, anon=True)
    except Exception as e:
        print('Error: ', e)
    print("Done")
    return format(image['link'])


# The following is for testing of imgur uploads
if __name__ == "__main__":
    # Any python file wishing to call the upload_image function must include the following imports:
    from imgur.imgur_settings import client_id, client_secret
    from imgurpython import ImgurClient

    imgur_client = ImgurClient(client_id, client_secret)
    image_path = 'test.png'
    image_url = upload_image(imgur_client, image_path)

    print("Image posted. Here is the link: ", image_url)
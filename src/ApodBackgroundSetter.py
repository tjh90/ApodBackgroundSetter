import os

import requests

import ApodApiRequest
import BackgroundSetter

if __name__ == '__main__':

    # Get the API key from a .env file.
    env_file = '.env'
    if os.path.isfile(env_file):
        with open(env_file) as file:
            api_key = file.readline().strip()

    # Get the image URL by querying the APOD API.
    image_url = ApodApiRequest.get_apod_image_url(api_key)
    if image_url is not None:
        response = requests.get(image_url)
        if requests.codes.ok != response.status_code:
            response.raise_for_status()

        # Generate the file name from the image URL.
        extension = image_url.split('.')[-1]
        img_file = f'img.{extension}'

        # Download the image and save it to a file.
        with open(img_file, 'wb') as file:
            file.write(response.content)

        # Set the background image.
        BackgroundSetter.set_background_image(img_file)

import ApodApiRequest
import BackgroundSetter

import os
import requests

if __name__ == '__main__':

    # Get the API key from a .env file.
    envFile = '.env'
    if os.path.isfile(envFile):
        with open(envFile, 'r') as file:
            apiKey = file.readline().strip()

    # Get the image URL by querying the APOD API.
    imageUrl = ApodApiRequest.GetApodImageUrl(apiKey)
    response = requests.get(imageUrl)
    if requests.codes.ok != response.status_code:
        response.raise_for_status()

    # Generate the file name from the image URL.
    extension = imageUrl.split('.')[-1]
    imgFile = f'img.{extension}'

    # Download the image and save it to a file.
    with open(imgFile, 'wb') as file:
        file.write(response.content)

    # Set the background image.
    BackgroundSetter.SetBackgroundImage(imgFile)

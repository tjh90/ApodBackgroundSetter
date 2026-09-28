import os

import requests

import ApodApiRequest
import BackgroundSetter


def _is_supported_image_url(url: str) -> bool:
    return url.startswith("https://") and "." in url


if __name__ == "__main__":
    # Get the API key from a .env file.
    env_file = ".env"
    if os.path.isfile(env_file):
        with open(env_file) as file:
            api_key = file.readline().strip()

    # Get the image URL by querying the APOD API.
    image_url = ApodApiRequest.get_apod_image_url(api_key)
    if image_url is not None and _is_supported_image_url(image_url):
        response = requests.get(image_url, timeout=30)
        if requests.codes.ok != response.status_code:
            response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            raise ValueError("APOD URL did not return image content.")

        # Generate the file name from the image URL.
        extension = image_url.split(".")[-1]
        img_file = f"img.{extension}"

        # Download the image and save it to a file.
        with open(img_file, "wb") as file:
            file.write(response.content)

        # Set the background image.
        BackgroundSetter.set_background_image(img_file)

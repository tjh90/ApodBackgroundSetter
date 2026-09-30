import os
import urllib.parse

import requests

import ApodApiRequest
import BackgroundSetter


def _is_supported_image_url(url: str) -> bool:
    return url.startswith("https://") and "." in url


def _get_image_extension(image_url: str) -> str | None:
    # The hdurl is a dynamic image URL carrying a query string (for example
    # "?w=1772&h=1182"), so the extension has to be read from the path.
    path = urllib.parse.urlparse(image_url).path
    return os.path.splitext(path)[1].lstrip(".")


if __name__ == "__main__":
    # Get the image URL by querying the APOD API.
    image_url = ApodApiRequest.get_apod_image_url()
    if image_url is not None and _is_supported_image_url(image_url):
        response = requests.get(image_url, timeout=30)
        if requests.codes.ok != response.status_code:
            response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            raise ValueError("APOD URL did not return image content.")

        # Generate the file name from the image URL.
        extension = _get_image_extension(image_url)
        if not extension:
            raise ValueError("Failed to determine image extension.")
        img_file = f"img.{extension}"

        # Download the image and save it to a file.
        with open(img_file, "wb") as file:
            file.write(response.content)

        # Set the background image.
        BackgroundSetter.set_background_image(img_file)

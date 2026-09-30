import datetime

import requests

_apod_api_base_url = "https://science.nasa.gov/wp-json/wp/v2/apod-basic"

_apod_date_path_format = "%y%m%d"

_apod_response_media_type_key = "media_type"
_apod_response_hd_url_key = "hdurl"

_apod_response_media_type_image = "image"


def _get_apod_url(apod_date: datetime.date) -> str:
    """
    Build the APOD API URL for the entry published on the given date.

    The endpoint identifies an entry by a six digit YYMMDD path segment.

    Args:
        apod_date (datetime.date): The date of the APOD to request.
    Returns:
        str: The URL of the APOD API endpoint for that date.
    """

    return f"{_apod_api_base_url}/{apod_date.strftime(_apod_date_path_format)}"


def get_apod_image_url(apod_date: datetime.date | None = None) -> str | None:
    """
    Make a request to NASA's Astronomy Picture of the Day (APOD) API to get the URL of the given day's picture.

    Args:
        apod_date (Optional[datetime.date]): The date of the APOD to fetch. Defaults to the current local date.
    Returns:
        Optional[str]: The URL of the HD image for the given day's APOD if it is an image, otherwise None.
    Raises:
        requests.HTTPError: If the request to the APOD API fails.
    """

    if apod_date is None:
        apod_date = datetime.date.today()

    # Make the request to the APOD API.
    response = requests.get(_get_apod_url(apod_date))

    # Raise an HTTPError if the request was not successful.
    if requests.codes.ok != response.status_code:
        response.raise_for_status()

    # Parse the JSON response and check the media type.
    json_response = response.json()
    media_type = json_response.get(_apod_response_media_type_key, None)
    if _apod_response_media_type_image != media_type:
        # APOD is not an image that day (it is probably a video).
        return None

    return json_response.get(_apod_response_hd_url_key, None)

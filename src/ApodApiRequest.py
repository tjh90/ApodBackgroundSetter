
import requests

_apod_api_base_url = 'https://api.nasa.gov/planetary/apod'
_apod_request_param_api_key = 'api_key'

_apod_response_media_type_key = 'media_type'
_apod_response_hd_url_key = 'hdurl'

_apod_response_media_type_image = 'image'

def get_apod_image_url(api_key: str) -> str | None:
    '''
    Make a request to NASA's Astronomy Picture of the Day (APOD) API to get the URL of today's picture.

    Args:
        apiKey (str): The NASA API key to use in the request.
    Returns:
        Optional[str]: The URL of the HD image for today's APOD if it is an image, otherwise None.
    Raises:
        requests.HTTPError: If the request to the APOD API fails.
    '''

    # Make the request to the APOD API.
    url = f"{_apod_api_base_url}?{_apod_request_param_api_key}={api_key}"
    response = requests.get(url)

    # Raise an HTTPError if the request was not successful.
    if requests.codes.ok != response.status_code:
        response.raise_for_status()

    # Parse the JSON response and check the media type.
    json_response = response.json()
    media_type = json_response.get(_apod_response_media_type_key, None)
    if _apod_response_media_type_image != media_type:
        # APOD is not an image today (it is probably a video).
        return None

    return json_response.get(_apod_response_hd_url_key, None)

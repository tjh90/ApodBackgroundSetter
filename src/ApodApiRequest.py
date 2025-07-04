from typing import Optional

import requests

_apodApiBaseUrl = 'https://api.nasa.gov/planetary/apod'
_apodRequestParamApiKey = 'api_key'

_apodResponseMediaTypeKey = 'media_type'
_apodResponseHdUrlKey = 'hdurl'

_apodResponseMediaTypeImage = 'image'

def GetApodImageUrl(apiKey: str) -> Optional[str]:
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
    url = f"{_apodApiBaseUrl}?{_apodRequestParamApiKey}={apiKey}"
    response = requests.get(url)

    # Raise an HTTPError if the request was not successful.
    if requests.codes.ok != response.status_code:
        response.raise_for_status()

    # Parse the JSON response and check the media type.
    jsonResponse = response.json()
    mediaType = jsonResponse.get(_apodResponseMediaTypeKey, None)
    if _apodResponseMediaTypeImage != mediaType:
        # APOD is not an image today (it is probably a video).
        return None

    return jsonResponse.get(_apodResponseHdUrlKey, None)

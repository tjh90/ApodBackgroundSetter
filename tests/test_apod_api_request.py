import unittest
from unittest.mock import Mock, patch

import requests

import ApodApiRequest

_API_KEY = 'DEMO_KEY'

def _make_response(status_code=200, json_data=None, http_error=None):
    response = Mock(spec=requests.Response)
    response.status_code = status_code
    response.json.return_value = json_data
    if http_error is not None:
        response.raise_for_status.side_effect = http_error

    return response

class GetApodImageUrlTest(unittest.TestCase):

    def test_returns_hdurl_for_an_image(self):
        response = _make_response(json_data={
            'media_type': 'image',
            'url': 'https://apod.nasa.gov/apod/image/sd.jpg',
            'hdurl': 'https://apod.nasa.gov/apod/image/hd.jpg',
        })

        with patch.object(ApodApiRequest.requests, 'get', return_value=response) as get:
            result = ApodApiRequest.get_apod_image_url(_API_KEY)

        self.assertEqual(result, 'https://apod.nasa.gov/apod/image/hd.jpg')
        get.assert_called_once_with(f'https://api.nasa.gov/planetary/apod?api_key={_API_KEY}')
        response.raise_for_status.assert_not_called()

    def test_returns_none_when_media_type_is_missing(self):
        response = _make_response(json_data={'title': 'Some title', 'hdurl': 'hd.jpg'})

        with patch.object(ApodApiRequest.requests, 'get', return_value=response):
            result = ApodApiRequest.get_apod_image_url(_API_KEY)

        self.assertIsNone(result)
        response.raise_for_status.assert_not_called()

    def test_returns_none_for_a_video(self):
        response = _make_response(json_data={'media_type': 'video'})

        with patch.object(ApodApiRequest.requests, 'get', return_value=response):
            result = ApodApiRequest.get_apod_image_url(_API_KEY)

        self.assertIsNone(result)
        response.raise_for_status.assert_not_called()

    def test_returns_none_when_media_type_is_an_unknown_value(self):
        response = _make_response(json_data={'media_type': 'gif', 'hdurl': 'hd.gif'})

        with patch.object(ApodApiRequest.requests, 'get', return_value=response):
            result = ApodApiRequest.get_apod_image_url(_API_KEY)

        self.assertIsNone(result)
        response.raise_for_status.assert_not_called()

    def test_returns_none_when_hdurl_is_missing(self):
        response = _make_response(json_data={
            'media_type': 'image',
            'url': 'https://apod.nasa.gov/apod/image/low.jpg',
        })

        with patch.object(ApodApiRequest.requests, 'get', return_value=response):
            result = ApodApiRequest.get_apod_image_url(_API_KEY)

        self.assertIsNone(result)
        response.raise_for_status.assert_not_called()

    def test_raises_http_error_on_a_failed_request(self):
        for status_code in (400, 401, 429, 500, 503):
            with self.subTest(status_code=status_code):
                error = requests.HTTPError(f'{status_code} Server Error')
                response = _make_response(status_code=status_code, http_error=error)

                with patch.object(ApodApiRequest.requests, 'get', return_value=response):
                    with self.assertRaises(requests.HTTPError):
                        ApodApiRequest.get_apod_image_url(_API_KEY)

                response.raise_for_status.assert_called_once()

    def test_does_not_parse_the_body_of_a_failed_request(self):
        response = _make_response(
            status_code=500, http_error=requests.HTTPError('500 Server Error'))

        with patch.object(ApodApiRequest.requests, 'get', return_value=response):
            with self.assertRaises(requests.HTTPError):
                ApodApiRequest.get_apod_image_url(_API_KEY)

        response.json.assert_not_called()
        response.raise_for_status.assert_called_once()

if __name__ == '__main__':
    unittest.main()

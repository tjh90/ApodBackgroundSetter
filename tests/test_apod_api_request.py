import datetime
import unittest
from unittest.mock import Mock, patch

import requests

import ApodApiRequest

_APOD_API_BASE_URL = ApodApiRequest._apod_api_base_url
_APOD_DATE = datetime.date(2026, 9, 30)
_APOD_DATE_PATH = "260930"
_APOD_URL = f"{_APOD_API_BASE_URL}/{_APOD_DATE_PATH}"


def _make_response(status_code=200, json_data=None, http_error=None):
    response = Mock(spec=requests.Response)
    response.status_code = status_code
    response.json.return_value = json_data
    if http_error is not None:
        response.raise_for_status.side_effect = http_error

    return response


class GetApodUrlTest(unittest.TestCase):
    def test_builds_a_six_digit_yymmdd_path(self):
        self.assertEqual(ApodApiRequest._get_apod_url(_APOD_DATE), _APOD_URL)

    def test_zero_pads_single_digit_month_and_day(self):
        url = ApodApiRequest._get_apod_url(datetime.date(2026, 1, 2))

        self.assertEqual(url, f"{_APOD_API_BASE_URL}/260102")

    def test_uses_a_two_digit_year_across_centuries(self):
        for apod_date, expected in (
            (datetime.date(1999, 1, 1), "990101"),
            (datetime.date(2000, 1, 1), "000101"),
            (datetime.date(2068, 12, 31), "681231"),
        ):
            with self.subTest(apod_date=apod_date):
                self.assertEqual(
                    ApodApiRequest._get_apod_url(apod_date),
                    f"{_APOD_API_BASE_URL}/{expected}",
                )


class GetApodImageUrlTest(unittest.TestCase):
    def test_requests_the_given_date(self):
        response = _make_response(
            json_data={
                "media_type": "image",
                "url": "https://science.nasa.gov/image-article/apod-2026-september-30/",
                "hdurl": "https://assets.science.nasa.gov/dynamicimage/apod.jpg",
            }
        )

        with patch.object(ApodApiRequest.requests, "get", return_value=response) as get:
            result = ApodApiRequest.get_apod_image_url(_APOD_DATE)

        self.assertEqual(
            result, "https://assets.science.nasa.gov/dynamicimage/apod.jpg"
        )
        get.assert_called_once_with(_APOD_URL)
        response.raise_for_status.assert_not_called()

    def test_requests_todays_date_by_default(self):
        response = _make_response(json_data={"media_type": "image", "hdurl": "hd.jpg"})

        with (
            patch.object(ApodApiRequest.requests, "get", return_value=response) as get,
            patch.object(ApodApiRequest.datetime, "date") as mock_date,
        ):
            mock_date.today.return_value = _APOD_DATE
            result = ApodApiRequest.get_apod_image_url()

        self.assertEqual(result, "hd.jpg")
        get.assert_called_once_with(_APOD_URL)

    def test_returns_none_when_media_type_is_missing(self):
        response = _make_response(json_data={"title": "Some title", "hdurl": "hd.jpg"})

        with patch.object(ApodApiRequest.requests, "get", return_value=response):
            result = ApodApiRequest.get_apod_image_url(_APOD_DATE)

        self.assertIsNone(result)
        response.raise_for_status.assert_not_called()

    def test_returns_none_for_a_video(self):
        response = _make_response(json_data={"media_type": "video"})

        with patch.object(ApodApiRequest.requests, "get", return_value=response):
            result = ApodApiRequest.get_apod_image_url(_APOD_DATE)

        self.assertIsNone(result)
        response.raise_for_status.assert_not_called()

    def test_returns_none_for_an_iframe(self):
        response = _make_response(json_data={"media_type": "iframe"})

        with patch.object(ApodApiRequest.requests, "get", return_value=response):
            result = ApodApiRequest.get_apod_image_url(_APOD_DATE)

        self.assertIsNone(result)
        response.raise_for_status.assert_not_called()

    def test_returns_none_when_media_type_is_an_unknown_value(self):
        response = _make_response(json_data={"media_type": "gif", "hdurl": "hd.gif"})

        with patch.object(ApodApiRequest.requests, "get", return_value=response):
            result = ApodApiRequest.get_apod_image_url(_APOD_DATE)

        self.assertIsNone(result)
        response.raise_for_status.assert_not_called()

    def test_returns_none_when_hdurl_is_missing(self):
        response = _make_response(
            json_data={
                "media_type": "image",
                "url": "https://science.nasa.gov/image-article/apod-2026-september-30/",
            }
        )

        with patch.object(ApodApiRequest.requests, "get", return_value=response):
            result = ApodApiRequest.get_apod_image_url(_APOD_DATE)

        self.assertIsNone(result)
        response.raise_for_status.assert_not_called()

    def test_raises_http_error_on_a_failed_request(self):
        for status_code in (400, 404, 429, 500, 503):
            with self.subTest(status_code=status_code):
                error = requests.HTTPError(f"{status_code} Server Error")
                response = _make_response(status_code=status_code, http_error=error)

                with (
                    patch.object(ApodApiRequest.requests, "get", return_value=response),
                    self.assertRaises(requests.HTTPError),
                ):
                    ApodApiRequest.get_apod_image_url(_APOD_DATE)

                response.raise_for_status.assert_called_once()

    def test_does_not_parse_the_body_of_a_failed_request(self):
        response = _make_response(
            status_code=404, http_error=requests.HTTPError("404 Not Found")
        )

        with (
            patch.object(ApodApiRequest.requests, "get", return_value=response),
            self.assertRaises(requests.HTTPError),
        ):
            ApodApiRequest.get_apod_image_url(_APOD_DATE)

        response.json.assert_not_called()
        response.raise_for_status.assert_called_once()


if __name__ == "__main__":
    unittest.main()

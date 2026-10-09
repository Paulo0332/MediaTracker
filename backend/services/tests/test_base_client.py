from services.api_clients.base import BaseApiClient, ApiClientError, ApiNetworkError, ApiStatusError, ApiTimeoutError
from django.test import SimpleTestCase
from unittest.mock import patch,MagicMock
import httpx

class TestBaseApiClient(SimpleTestCase):
    def setUp(self):
        self.default_client = BaseApiClient(base_url="https://api.themoviedb.org/3/", auth_token="placeholder")
    
    def test_base_url_parsing_with_slash(self):
        custom_url = BaseApiClient(base_url="https://api.themoviedb.org/3/",auth_token="placeholder")
        self.assertEqual(custom_url.base_url,"https://api.themoviedb.org/3")

    def test_base_url_parsing_without_slash(self):
        custom_url = BaseApiClient(base_url="https://api.themoviedb.org/3",auth_token="placeholder")
        self.assertEqual(custom_url.base_url,"https://api.themoviedb.org/3")

    @patch("httpx.Client.request")
    def test_endpoint_normalization_with_slash(self, mock_httpx_request: MagicMock):
        fake_response = MagicMock()
        fake_response.status_code = 200
        fake_response.json.return_value = {"results" : []}
        mock_httpx_request.return_value = fake_response

        self.default_client._request(method= "GET", endpoint="/movie/popular", params=None, json_data=None)

        mock_httpx_request.assert_called_once_with(
            method="GET", url="/movie/popular", params=None, json=None
        )

    @patch("httpx.Client.request")
    def test_endpoint_normalization_without_slash(self, mock_httpx_request: MagicMock):
        fake_response = MagicMock()
        fake_response.status_code = 200
        fake_response.json.return_value = {"results" : []}
        mock_httpx_request.return_value = fake_response

        self.default_client._request(method= "GET", endpoint="movie/popular", params=None, json_data=None)

        mock_httpx_request.assert_called_once_with(
            method="GET", url="/movie/popular", params=None, json=None
        )

    @patch("httpx.Client.request")
    def test_request_success_return_parsed_json(self, mock_httpx_request: MagicMock):
        expected_payload = {"key":"value", "items":[1,2,3]}
        
        fake_response = MagicMock()
        fake_response.status_code = 200
        fake_response.json.return_value = expected_payload
        mock_httpx_request.return_value = fake_response

        result = self.default_client._request(method="GET",endpoint="placeholder")
        self.assertEqual(result,expected_payload)

    @patch("httpx.Client.request")
    def test_request_timeout_raises_api_timeout_error(self, mock_httpx_request: MagicMock):
        mock_httpx_request.side_effect = httpx.TimeoutException(message="Connection timed out")

        with self.assertRaises(ApiTimeoutError) as cm:
            self.default_client._request(method="GET",endpoint="placeholder")

        self.assertEqual(str(cm.exception),"The API timed out at [/placeholder]")
        
    @patch("httpx.Client.request")
    def test_request_status_error_raises_api_status_error(self, mock_httpx_request: MagicMock):
        mock_httpx_request.side_effect = httpx.HTTPStatusError(
            message="Status error",
            request= MagicMock(spec=httpx.Request), 
            response= MagicMock(spec=httpx.Response, status_code = 500)
        )

        with self.assertRaises(ApiStatusError) as cm:
            self.default_client._request(method="GET",endpoint="placeholder")

        self.assertEqual(str(cm.exception),"The API returned status 500 for [/placeholder]") 

    @patch("httpx.Client.request")
    def test_request_network_error_raises_api_network_error(self, mock_httpx_request: MagicMock):
        mock_httpx_request.side_effect = httpx.RequestError(message="Network error", request= MagicMock(spec=httpx.Request))

        with self.assertRaises(ApiNetworkError) as cm:
            self.default_client._request(method="GET",endpoint="placeholder")

        self.assertEqual(str(cm.exception),"Transport network error at [/placeholder]: Network error")

    def test_derived_exceptions_inherit_from_base_error(self):
        self.assertTrue(issubclass(ApiStatusError, ApiClientError))
        self.assertTrue(issubclass(ApiNetworkError, ApiClientError))
        self.assertTrue(issubclass(ApiTimeoutError, ApiClientError))

    @patch("httpx.Client.close")
    def test_close_terminates_session(self, mock_httpx_close: MagicMock):
        self.default_client.close()
        mock_httpx_close.assert_called_once()
        
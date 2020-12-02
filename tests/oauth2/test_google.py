from typing import Dict
import pytest

from flask_jwt_router.oauth2._exceptions import RequestAttributeError, ClientExchangeCodeError
from flask_jwt_router.oauth2.google import Google, _FlaskRequestType
from flask_jwt_router.oauth2.http_requests import HttpRequests
from flask_jwt_router.oauth2._urls import GOOGLE_OAUTH_URL
from tests.fixtures.oauth_fixtures import TEST_OAUTH_URL, http_requests

mock_exchange_response = {
    "access_token": "<access_token>",
    "expires_in": 3920,
    "token_type": "Bearer",
    "scope": "https://www.googleapis.com/auth/drive.metadata.readonly",
    "refresh_token": "<refresh_token>"
}

_mock_client_post = {
    "code": "<CODE>",
    "scope": "<SCOPE>",
    "email": "<EMAIL>"
}


class _MockFlaskRequest(_FlaskRequestType):

    base_url = "http://localhost:3000/google_login"

    _mock_client_post = {
        "code": "<CODE>",
        "scope": "<SCOPE>",
        "email": "<EMAIL>"
    }

    @staticmethod
    def get_json() -> Dict:
        return _mock_client_post


class TestGoogle:

    mock_options = {
        "client_id": "<CLIENT_ID>",
        "client_secret": "<CLIENT_SECRET>",
        "redirect_uri": "http://localhost:3000",
        "tablename": "users",
        "email_field": "email",
        "expires_in": 3600,
    }

    def test_google(self, http_requests):
        g = Google(http_requests())
        g.init(**self.mock_options)
        assert hasattr(g, "client_id")
        assert hasattr(g, "client_secret")
        assert hasattr(g, "grant_type")
        assert hasattr(g, "redirect_uri")
        assert hasattr(g, "tablename")
        assert hasattr(g, "email_field")
        assert hasattr(g, "expires_in")

    def test_update_base_path(self, http_requests):

        g = Google(http_requests())
        g.init(**self.mock_options)
        g.code = "<CODE>"
        g._url = "https://oauth2.googleapis.com/token"
        g.update_base_path(g._url)
        expected = "https://oauth2.googleapis.com/token?" \
                   "code=<CODE>&" \
                   "client_id=<CLIENT_ID>&" \
                   "client_secret=<CLIENT_SECRET>&" \
                   "redirect_uri=http://localhost:3000&" \
                   "grant_type=authorization_code&" \
                   "expires_in=3600"
        assert g._url == expected

    def test_oauth_login_raises(self, http_requests):
        g = Google(http_requests())
        g.init(**self.mock_options)
        with pytest.raises(RequestAttributeError):
            _ = g.oauth_login(None)

    def test_oauth_login_no_code_raises(self, http_requests):
        g = Google(http_requests(None))
        g.init(**self.mock_options)
        request = _MockFlaskRequest()
        def get_json():
            return {}
        setattr(request, "get_json", get_json)
        with pytest.raises(ClientExchangeCodeError):
            _ = g.oauth_login(request)

    def test_oauth_login(self, http_requests):
        g = Google(http_requests())
        g.init(**self.mock_options)
        result = g.oauth_login(_MockFlaskRequest())
        assert result["access_token"] == "<access_token>"

    @pytest.mark.skip
    def test_authorize(self, http_requests):
        """
        {
          "family_name": "",
          "name": "",
          "picture": "",
          "locale": "en",
          "email": "",
          "given_name": "Joe",
          "id": "",
          "verified_email": true
        }
        """
        g = Google(http_requests(GOOGLE_OAUTH_URL))
        g.init(**self.mock_options)
        token = ""
        result = g.authorize(token)
        assert "email" in result

    @pytest.mark.skip
    def test_local_oauth_login(self):
        class _Request(_FlaskRequestType):  # TODO make into fixture
            base_url = "http://localhost:3000/google_login"

            @staticmethod
            def get_json() -> Dict:
                return {
                    "code": "",
                    "scope": "",
                }

        g = Google(http_requests(GOOGLE_OAUTH_URL))
        g.init(**{
            "client_id": "",
            "client_secret": "",
            "redirect_uri": "",
        })
        result = g.oauth_login(_Request())

from typing import Dict
import pytest

from flask_jwt_router.oauth2._exceptions import RequestAttributeError, ClientExchangeCodeError
from flask_jwt_router.oauth2.google import Google, _FlaskRequestType
from flask_jwt_router.oauth2.http_requests import HttpRequests


_mock_exchange_response = {
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


class _MockHttpRequests:
    code: str

    def __init__(self, code="<CODE>"):
        self.code = code

    def post_token(self, url: str, token: str = None):
        return _mock_exchange_response

    def get_by_scope(self, scope_url: str, access_token: str):
        pass


class _MockFlaskRequest(_FlaskRequestType):

    base_url = "http://localhost:3000/google_login"

    @staticmethod
    def get_json() -> Dict:
        return _mock_client_post


class TestGoogle:

    mock_options = {
        "client_id": "<CLIENT_ID>",
        "client_secret": "<CLIENT_SECRET>",
        "redirect_uri": "http://localhost:3000",
    }

    def test_google(self):
        g = Google(_MockHttpRequests)
        g.init(**self.mock_options)
        assert hasattr(g, "client_id")
        assert hasattr(g, "client_secret")
        assert hasattr(g, "grant_type")
        assert hasattr(g, "redirect_uri")

    def test_create_url(self):

        g = Google(_MockHttpRequests)
        g.init(**self.mock_options)
        g.code = "<CODE>"
        result = g.create_url()
        expected = "https://oauth2.googleapis.com/token?" \
                   "code=<CODE>&" \
                   "client_id=<CLIENT_ID>&" \
                   "client_secret=<CLIENT_SECRET>&" \
                   "redirect_uri=http://localhost:3000&grant_type=authorization_code"
        assert result == expected

    def test_oauth_login_raises(self):
        g = Google(_MockHttpRequests)
        g.init(**self.mock_options)
        with pytest.raises(RequestAttributeError):
            _ = g.oauth_login(None)

    def test_oauth_login_no_code_raises(self):
        g = Google(_MockHttpRequests(None))
        g.init(**self.mock_options)
        request = _MockFlaskRequest()
        def get_json():
            return {}
        setattr(request, "get_json", get_json)
        with pytest.raises(ClientExchangeCodeError):
            _ = g.oauth_login(request)

    def test_oauth_login(self):
        g = Google(_MockHttpRequests())
        g.init(**self.mock_options)
        result = g.oauth_login(_MockFlaskRequest())
        assert result["access_token"] == "<access_token>"

from typing import Dict
import pytest

from flask_jwt_router.oauth2._exceptions import RequestAttributeError, ClientExchangeCodeError
from flask_jwt_router.oauth2.google import Google, _FlaskRequestType
from flask_jwt_router.oauth2.http_requests import HttpRequests
from flask_jwt_router.oauth2._urls import GOOGLE_OAUTH_URL
from tests.fixtures.oauth_fixtures import TEST_OAUTH_URL, http_requests
from tests.fixtures.model_fixtures import MockAOuthModel

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
        g.update_base_path(g._url, "http://localhost:3000")
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
        # TODO better tests
        g.oauth_login(_MockFlaskRequest(), redirect_uri="<new_redirect_uri>")
        g.update_base_path("<url>", "<new_redirect_uri>")
        assert "<new_redirect_uri>" in g._url

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

    def test_create_test_headers(self, http_requests, MockAOuthModel):

        mock_user = MockAOuthModel(email="test@email.com")
        g = Google(http_requests(GOOGLE_OAUTH_URL))
        g.init(**self.mock_options)

        result = g.create_test_headers(email="test@email.com")
        assert result == {'X-Auth-Token': 'Bearer test@email.com'}
        assert g.test_metadata["test@email.com"]["email"] == "test@email.com"
        assert g.test_metadata["test@email.com"]["entity"] is None
        assert g.test_metadata["test@email.com"]["scope"] is "function"

        result = g.create_test_headers(email="test@email.com", entity=mock_user)
        assert result == {'X-Auth-Token': 'Bearer test@email.com'}
        assert g.test_metadata["test@email.com"]["email"] == "test@email.com"
        assert g.test_metadata["test@email.com"]["entity"] == mock_user
        assert g.test_metadata["test@email.com"]["scope"] is "function"

        result = g.create_test_headers(email="test@email.com", entity=mock_user, scope="application")
        assert result == {'X-Auth-Token': 'Bearer test@email.com'}
        assert g.test_metadata["test@email.com"]["email"] == "test@email.com"
        assert g.test_metadata["test@email.com"]["entity"] == mock_user
        assert g.test_metadata["test@email.com"]["scope"] is "application"

    def test_tear_down(self, http_requests, MockAOuthModel):
        mock_user = MockAOuthModel(email="test@email.com")
        g = Google(http_requests(GOOGLE_OAUTH_URL))
        g.init(**self.mock_options)

        result = g.create_test_headers(email="test@email.com", entity=mock_user, scope="application")
        assert result == {'X-Auth-Token': 'Bearer test@email.com'}
        assert g.test_metadata["test@email.com"]["email"] == "test@email.com"
        assert g.test_metadata["test@email.com"]["entity"] == mock_user
        assert g.test_metadata["test@email.com"]["scope"] is "application"
        g.tear_down()
        assert g.test_metadata["test@email.com"]["email"] == "test@email.com"
        g.tear_down(scope="application")
        assert g.test_metadata == {}

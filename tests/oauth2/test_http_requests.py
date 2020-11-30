import pytest

from flask_jwt_router.oauth2.http_requests import HttpRequests
from flask_jwt_router.oauth2._urls import GOOGLE_OAUTH_URL
from tests.mock_server.mock_server import server_thread
from tests.fixtures.oauth_fixtures import oauth_urls


class TestHttpRequests:

    def test_token(self, oauth_urls):
        h = HttpRequests(oauth_urls)
        server_thread.start()
        result = h.token(h.get_url("server_thread"))
        h.token(h.get_url("shut_down"))
        server_thread.join()
        assert result["access_token"] == "<access_token>"
        assert result["expires_in"] == 3920
        assert result["token_type"] == "Bearer"
        assert result["scope"] == "https://www.googleapis.com/auth/drive.metadata.readonly"
        assert result["refresh_token"] == "<refresh_token>"

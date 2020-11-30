import pytest


TEST_OAUTH_URL = {
    "local_flask": "http://localhost:5000/ibanez/api/v1/staffs/login",
    "server_thread": "http://localhost:5000/mock_google_exchange",
    "shut_down": "http://localhost:5000/shut_down",
    "token": "https://oauth2.googleapis.com/token",
    "user_info.email": "https://www.googleapis.com/oauth2/v2/userinfo",
}


@pytest.fixture
def oauth_urls():
    return TEST_OAUTH_URL


@pytest.fixture
def http_requests():
    def inner(_code="<CODE>"):
        class _MockHttpRequests:
            code: str

            urls = TEST_OAUTH_URL

            mock_exchange_response = {
                "access_token": "<access_token>",
                "expires_in": 3920,
                "token_type": "Bearer",
                "scope": "https://www.googleapis.com/auth/drive.metadata.readonly",
                "refresh_token": "<refresh_token>"
            }

            def __init__(self, code):
                self.code = code

            def get_url(self, name):
                return self.urls[name]

            def token(self, url: str, token: str = None):
                return self.mock_exchange_response

            def get_by_scope(self, scope_url: str, access_token: str):
                return {
                      "family_name": "Pastorius",
                      "name": "Jaco Pastorius",
                      "picture": "https://lh3.googleusercontent.com/a-/lalalala",
                      "locale": "en",
                      "email": "jaco@gmail.com",
                      "given_name": "Jaco",
                      "id": "1234567890",
                      "verified_email": True
                }
        return _MockHttpRequests(_code)
    return inner

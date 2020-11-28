from typing import Dict
from abc import ABC, abstractmethod

from .http_requests import HttpRequests
from ._base import BaseOAuth
from ._exceptions import RequestAttributeError, ClientExchangeCodeError


class _FlaskRequestType(ABC):

    base_url = None

    @staticmethod
    @abstractmethod
    def get_json() -> Dict:
        pass


class Google(BaseOAuth):
    #: As defined in https://tools.ietf.org/html/rfc6749#section-4.1.3
    #: Value MUST be set to "authorization_code".
    grant_type = "authorization_code"

    base = "https://oauth2.googleapis.com/token"

    client_id: str

    client_secret: str

    _code: str

    redirect_uri: str

    _access_token_url: str


    scopes = {
        "user_info.email": "https://www.googleapis.com/auth/userinfo.email",
    }

    user_info_url: str = "https://www.googleapis.com/auth/"

    http: HttpRequests

    def __init__(self, http):
        self.http = http

    @property
    def access_token_url(self):
        return self._access_token_url

    @access_token_url.setter
    def access_token_url(self, val):
        self._access_token_url = val

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, val):
        self._code = val

    def init(self, *, client_id, client_secret, redirect_uri) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def create_url(self) -> str:
        url = f"{self.base}?"
        url = f"{url}code={self.code}&"
        url = f"{url}client_id={self.client_id}&"
        url = f"{url}client_secret={self.client_secret}&"
        url = f"{url}redirect_uri={self.redirect_uri}&"
        url = f"{url}grant_type={self.grant_type}"
        return url

    def _exchange_auth_access_code(self) -> Dict:
        """
        :return:
            {
              "access_token": "<access_token>",
              "expires_in": 3920,
              "token_type": "Bearer",
              "scope": "https://www.googleapis.com/auth/drive.metadata.readonly",
              "refresh_token": "<refresh_token>"
            }
        """
        data = self.http.post_token(self.access_token_url)
        return data

    def oauth_login(self, request: _FlaskRequestType) -> str:
        if not request:
            raise RequestAttributeError()
        req_data = request.get_json()
        self.code = req_data.get("code")
        if not self.code:
            raise ClientExchangeCodeError(request.base_url)
        self.access_token_url = self.create_url()
        data = self._exchange_auth_access_code()
        res_data = {
            "access_token": data["access_token"],
        }
        return res_data

    def oauth_refresh(self, request: _FlaskRequestType):
        pass

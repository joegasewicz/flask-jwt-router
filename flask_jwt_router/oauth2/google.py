from typing import Dict
from abc import ABC, abstractmethod

from ._oath2 import OAuthTwo
from ._base import BaseOAuth
from ._exceptions import RequestAttributeError


class _FlaskRequestType(ABC):

    @abstractmethod
    def get_json(self) -> Dict:
        pass


class Google(BaseOAuth, OAuthTwo):
    #: As defined in https://tools.ietf.org/html/rfc6749#section-4.1.3
    #: Value MUST be set to "authorization_code".
    grant_type = "authorization_code"

    base = "https://oauth2.googleapis.com/token"

    client_id: str

    client_secret: str

    code: str

    redirect_uri: str

    access_token_url: str

    scopes = {
        "user_info.email": "https://www.googleapis.com/auth/userinfo.email",
    }

    user_info_url: str = "https://www.googleapis.com/auth/"

    def init(self, *, client_id, client_secret, code, redirect_uri) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.code = code
        self.redirect_uri = redirect_uri
        self.access_token_url = self._create_url()

    def _create_url(self) -> str:
        url = f"{self.base}?"
        url = f"{url}code={self.code}&"
        url = f"{url}client_id={self.client_id}&"
        url = f"{url}client_secret={self.client_secret}&"
        url = f"{url}redirect_uri={self.redirect_uri}&"
        url = f"{url}grant_type={self.grant_type}"
        return url

    def _exchange_auth_access_code(self, token) -> Dict:
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
        data = self.post_token(self.access_token_url, token)
        return data

    def oauth_login(self, request: _FlaskRequestType) -> str:
        if not request:
            raise RequestAttributeError()
        req_data = request.get_json()
        data = self._exchange_auth_access_code(req_data)
        res_data = {
            "access_token": data["access_token"],
        }
        return res_data

    def oauth_refresh(self, request: _FlaskRequestType):
        pass

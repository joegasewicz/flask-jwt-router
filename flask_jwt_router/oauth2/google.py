"""
    Google OAuth 2.0 Quick Start
    ============================

    Basic Usage::

        oauth_options = {
            "client_id": "<CLIENT_ID>",
            "client_secret": "<CLIENT_SECRET>",
            "redirect_uri": "http://localhost:3000",
            "tablename": "users",
            "email_field": "email",
            "expires_in": 3600,
        }

        jwt_routes.init_app(app, google_oauth=oauth_options)

"""
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

    #: Found in https://console.developers.google.com/apis/dashboard > Credentials > OAuth 2.0 Client IDs
    client_id: str

    #: Found in https://console.developers.google.com/apis/dashboard > Credentials > OAuth 2.0 Client IDs
    #: Never share this value with any client side code!
    client_secret: str

    #: This field must match exactly the client side redirect string.
    #: See https://console.developers.google.com/apis/dashboard >
    #: Credentials > OAuth 2.0 Client IDs. Click thru & match from the lists of the redirect domains
    redirect_uri: str

    #: OPTIONAL.  The lifetime in seconds of the access token.  For
    #: example, the value "3600" denotes that the access token will
    #: expire in one hour from the time the response was generated.
    expires_in: int

    #: Value of SQLAlchemy's __tablename__ attribute
    tablename: str

    #: Value of the email field column in the
    email_field: str

    _url: str

    _code: str

    http: HttpRequests

    _data: Dict

    def __init__(self, http):
        self.http = http

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, val):
        self._code = val

    def init(self, *, client_id, client_secret, redirect_uri, expires_in, email_field, tablename) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.expires_in = expires_in or self._set_expires()
        self.email_field = email_field
        self.tablename = tablename
        self._url = self.http.get_url("token")

    def update_base_path(self, path: str) -> None:
        url = f"{path}?"
        url = f"{url}code={self.code}&"
        url = f"{url}client_id={self.client_id}&"
        url = f"{url}client_secret={self.client_secret}&"
        url = f"{url}redirect_uri={self.redirect_uri}&"
        url = f"{url}grant_type={self.grant_type}&"
        url = f"{url}expires_in={self.expires_in}"
        self._url = url

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

        data = self.http.token(self._url)
        return data

    def oauth_login(self, request: _FlaskRequestType) -> Dict:
        """
        :param request: Flask request object
        :return Dict:
        """
        if not request:
            raise RequestAttributeError()
        req_data = request.get_json()
        self.code = req_data.get("code")
        if not self.code:
            raise ClientExchangeCodeError(request.base_url)
        # Add the rest of the param args to the base_path
        self.update_base_path(self._url)
        self._data = self._exchange_auth_access_code()
        res_data = {
            "access_token": self._data["access_token"],
        }
        return res_data

    def authorize(self, token: str):
        """
        Call to a Google API to authenticate via access_token
        """
        url = self.http.get_url("user_info.email")
        data = self.http.get_by_scope(url, token)
        return data

    def _set_expires(self):
        """
        The default expire is set to 7 days
        :return: None
        """
        self.expires_in = 3600 * 24 * 7

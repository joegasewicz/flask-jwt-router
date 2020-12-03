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

    Now your front end needs a token. Create an endpoint &
    return a new access token from the clients header *code*.
    For Example::

        from flask import request

        @app.routes("/login", methods=["POST"])
        def login():
            jwt_routes.google.oauth_login(request) # Pass in Flask's request

    Now, the next time your front-end requests authorised resources
    flask-jwt-router will authenticate with this access token until
    it expires.

    Flask-JWT-Router OAuth 2.0 Flow Explained
    =========================================

    Client
    ++++++

    If you're client is a React application, we strongly recommend you use React-Google-Oauth2
    https://github.com/joegasewicz/react-google-oauth2.0 It's maintain by Flask-JWT-Router's author,
    so if fully compatible.

    The *client* is your front end application, this could be another Flask api that
    renders jinja2 html templates or a React / Angular / Vue.js single page application.
    There are 2 steps that your client must successfully complete before Flask-JWT-Router
    can return a valid Google OAuth 2.0 access token.

    1.  The client must redirect the user to Googles sign in page. The user will then be
        asked to accept any extra scopes (Only required for advance access to Google Apis).
        If the user successfully signs in then Google will return a code to the client.

    2.  The client must now make a ``POST`` http request to your Flask api with Google's **code**
        in the **X-Auth-Token** header. For example

            curl -X POST -H "X-Auth-Token": "<YOUR_GOOGLE_OAUTH2.0_CODE>" http://localhost:5000/login

    Server
    ++++++

    **The server is your Flask app.** Now that your client has a code & has made the request to
    the server, we must provide a Flask view handler to exchange the client's code for an
    access token. Flask-JWT-Router has public method (See :obj:`~flask_jwt_router.oauth2.google.oauth_login`)
    that takes Flask's request as a single argument. If the Google OAuth2.0 **code** is valid, then a valid
    access token will be returned in the response body.

    For example::

        from flask import request

        @app.routes("/login", methods=["POST"])
        def login():
            data = jwt_routes.google.oauth_login(request) # Pass in Flask's request
            return data, 200

        # Returns:
        # {
        #   "access_token": "GOOGLE_OAUTH2.0_ACCESS_TOKEN>
        # }

    Each time the client requires any authorised resources in your Flask app, it must make all requests
    will the following headers::

        {
            "X-Auth-Token" : "<YOUR_GOOGLE_OAUTH2.0_CODE>"
        }

    This will allow the user to gain access to your Flask's app resources until the access token's
    expire time has ended. The client should then decide whether to redirect the user to Google's
    login screen.
"""
from typing import Dict
from abc import ABC, abstractmethod

from .http_requests import HttpRequests
from ._base import BaseOAuth, _FlaskRequestType
from ._exceptions import RequestAttributeError, ClientExchangeCodeError


class Google(BaseOAuth):
    #: As defined in https://tools.ietf.org/html/rfc6749#section-4.1.3
    #: Value MUST be set to "authorization_code".
    grant_type = "authorization_code"

    #: Found in https://console.developers.google.com/apis/dashboard > Credentials > OAuth 2.0 Client IDs
    client_id: str

    #: Found in https://console.developers.google.com/apis/dashboard > Credentials > OAuth 2.0 Client IDs
    #: Never share this value with any client side code!
    client_secret: str

    #: This field must match exactly the client side redirect string you have defined in
    #: *Google developer Credentials* page: See https://console.developers.google.com/apis/dashboard >
    #: Credentials > OAuth 2.0 Client IDs. Click thru & match from the lists of the redirect domains
    redirect_uri: str

    #: OPTIONAL. Default is 7 days. The lifetime in seconds of the access token.  For
    #: example, the value "3600" denotes that the access token will
    #: expire in one hour from the time the response was generated.
    expires_in: int = None

    #: Value of SQLAlchemy's __tablename__ attribute
    tablename: str

    #: Value of the email field column in the
    email_field: str

    _url: str = None

    _code: str = None

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

    def update_base_path(self, path: str) -> None:
        # TODO rename this method
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
        self._url = self.http.get_url("token")
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

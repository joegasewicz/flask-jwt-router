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

    If your app requires multiple redirect uri's then
    you can use the *redirect_uri* kwarg to assign a uri for the current
    request handler. For example::

        data = jwt_routes.google.oauth_login(request, redirect="http://another_redirect.com")


    Testing
    +++++++

    Testing OAuth2.0 in a Flask app is non-trivial, especially if you rely on Flask-JWT-Router
    to append your user onto Flask's global context (or `g`). Therefore we have provided a
    utility method that returns a headers Dict that you can then use in your test view handler
    request. This example is using the Pytest library::

        @pytest.fixture()
        def client():
            # See https://flask.palletsprojects.com/en/1.1.x/testing/ for details


        def test_blogs(client):
            user_headers = jwt_routes.google.create_test_headers(email="user@gmail.com")
            rv = client.get("/blogs", headers=user_headers)

    If you are not running a db in your tests, then you can use the `entity` kwarg.
    For example::

        # user is an instantiated SqlAlchemy object
        user_headers = jwt_routes.google.create_test_headers(email="user@gmail.com", entity=user)
        # user_headers: { "X-Auth-Token": "Bearer user@gmail.com" }

    If you require more than one request to a Flask view handler in a single unit test, then set
    the *scope* kwarg to **application**. (Default is *function*). If you are testing different
    entities within a single unit test method or function then you must pass in your entity.
    For example::

        my_entity = User(email="user@gmail.com") # If you're testing against a real db, make sure this is an entry in the db
        _ = jwt_routes.google.create_test_headers(email="user@gmail.com", scope="application", entity=my_entity)

"""
from typing import Dict, Optional, Tuple

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

    test_metadata: Dict[str, Dict[str, str]] = {}

    _current_test_email: str = None

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

    def oauth_login(self, request: _FlaskRequestType, **kwargs) -> Dict:
        """
        :param request: Flask request object
        :key redirect_uri: If your app requires multiple redirect uri's then
        you can use the *redirect_uri* kwarg to assign a uri for the current
        request handler. For example::

            data = jwt_routes.google.oauth_login(request, redirect="http://another_redirect.com")

        :return Dict:
        """
        redirect_uri = kwargs.get("redirect_uri")
        if redirect_uri:
            self.redirect_uri = redirect_uri
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

    def create_test_headers(self, *, email: str, entity=None, scope="function") -> Dict[str, str]:
        """
        :key email: SqlAlchemy object will be filtered against the email value.
        :key entity: Optional. SqlAlchemy object if you prefer not to run a db in your tests.
        :key scope: Optional. Default is *function*. Pass *application* if each unit test requires
        more than one request to a Flask view handler.

        If you are running your tests against a test db then just pass in the `email` kwarg.
        For example::

            user_headers = jwt_routes.google.create_test_headers(email="user@gmail.com")
            # user_headers: { "X-Auth-Token": "Bearer user@gmail.com" }

        If you are not running a db in your tests, then you can use the `entity` kwarg.
        For example::

            # user is an instantiated SqlAlchemy object
            user_headers = jwt_routes.google.create_test_headers(email="user@gmail.com", entity=user)
            # user_headers: { "X-Auth-Token": "Bearer user@gmail.com" }

        If you require more than one request to a Flask view handler in a single unit test, then set
        the *scope* kwarg to **application**.
        For example::

            _ = jwt_routes.google.create_test_headers(email="user@gmail.com", scope="application")


        :return: Python Dict containing header key value for OAuth routing with FJR
        """
        _meta = {
            "email": email,
            "entity": entity,
            "scope": scope,
        }
        self.test_metadata[f"{email}"] = _meta

        return {
            "X-Auth-Token": f"Bearer {email}",
        }

    def tear_down(self, *, scope: str = "function"):
        """
        If you are setting the *scope* to *application* in :class:`~flask_jwt_router.google.create_test_headers`
        then you may want to clean up the state outside or the teardown scope of your test runner
        (unittest or pytest etc.). Calling *tear_down()* will clean up the authorised OAuth state.
        For example::

            @pytest.fixture()
                def client():
                    ... # See https://flask.palletsprojects.com/en/1.1.x/testing/ for details
                    jwt_routes.google.tear_down(scope="application")

        :key scope: Optional. Default is *function*. Set to "application" to teardown all oauth state
        """
        if scope == "application":
            self.test_metadata = {}
        elif self._current_test_email in self.test_metadata:
            if self.test_metadata[self._current_test_email].get("scope") != "application":
                del self.test_metadata[self._current_test_email]

    def _update_test_metadata(self, email: str) -> Tuple[str, object]:
        """
        Updates test_metadata from passed values to create_test_headers
        :email: The email comes from the `Bearer <email>` token
        :private:
        :return:
        """
        self._current_test_email = email

        email = self.test_metadata[email]["email"]
        entity = self.test_metadata[email]["entity"]
        return email, entity

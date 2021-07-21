from ._base import BaseOAuth, _FlaskRequestType, TestBaseOAuth
from typing import Dict, Tuple
from flask_jwt_router.oauth2.google import Google


class GoogleTestUtil(Google, TestBaseOAuth):

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

    def update_test_metadata(self, email: str) -> Tuple[str, object]:
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

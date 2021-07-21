from flask import Flask
import pytest

from flask_jwt_router import JwtRoutes, GoogleTestUtil
from tests.fixtures.model_fixtures import MockEntityModel, MockAOuthModel


class TestJwtRoutes:

    oauth_options = {
        "client_id": "<CLIENT_ID>",
        "client_secret": "<CLIENT_SECRET>",
        "redirect_uri": "http://localhost:3000",
        "tablename": "users",
        "email_field": "email",
        "expires_in": 3600,
    }

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "__TEST_SECRET__"
    app.config["JWT_EXPIRE_DAYS"] = 8

    def test_init_app(self, MockEntityModel, MockAOuthModel):
        jwt = JwtRoutes(self.app, entity_models=[MockEntityModel])
        assert jwt.config.entity_models[0] == MockEntityModel
        assert jwt.app == self.app
        assert jwt.config.expire_days == 8

        jwt = JwtRoutes()
        jwt.init_app(self.app, entity_models=[MockEntityModel])
        assert jwt.config.entity_models[0] == MockEntityModel
        assert jwt.app == self.app
        assert jwt.config.expire_days == 8

        jwt = JwtRoutes(self.app)
        jwt.init_app(entity_models=[MockEntityModel])
        assert jwt.config.entity_models[0] == MockEntityModel
        assert jwt.app == self.app
        assert jwt.config.expire_days == 8

        jwt = JwtRoutes(entity_models=[MockEntityModel])
        jwt.init_app(self.app)
        assert jwt.config.entity_models[0] == MockEntityModel
        assert jwt.app == self.app
        assert jwt.config.expire_days == 8

        self.app.config["ENTITY_MODELS"] = [MockEntityModel]
        jwt = JwtRoutes()
        jwt.init_app(self.app)
        assert jwt.config.entity_models[0] == MockEntityModel
        assert jwt.app == self.app
        assert jwt.config.expire_days == 8

        self.app.config["ENTITY_MODELS"] = [MockEntityModel, MockAOuthModel]
        jwt = JwtRoutes()
        jwt.init_app(self.app, google_oauth=self.oauth_options, strategies=[GoogleTestUtil])
        assert jwt.config.entity_models[1] == MockAOuthModel
        assert jwt.config.google_oauth["client_id"] == "<CLIENT_ID>"
        assert jwt.config.google_oauth["client_secret"] == "<CLIENT_SECRET>"
        assert jwt.config.google_oauth["redirect_uri"] == "http://localhost:3000"
        assert jwt.config.google_oauth["tablename"] == "users"
        assert jwt.config.google_oauth["email_field"] == "email"
        assert jwt.config.google_oauth["expires_in"] == 3600

        self.app.config["ENTITY_MODELS"] = [MockEntityModel, MockAOuthModel]
        jwt = JwtRoutes(self.app, google_oauth=self.oauth_options, strategies=[GoogleTestUtil])
        jwt.init_app()
        assert jwt.config.entity_models[1] == MockAOuthModel
        assert jwt.config.google_oauth["client_id"] == "<CLIENT_ID>"
        assert jwt.config.google_oauth["client_secret"] == "<CLIENT_SECRET>"
        assert jwt.config.google_oauth["redirect_uri"] == "http://localhost:3000"
        assert jwt.config.google_oauth["tablename"] == "users"
        assert jwt.config.google_oauth["email_field"] == "email"
        assert jwt.config.google_oauth["expires_in"] == 3600

    def test_get_secret_key(self):
        class App:
            config = {
                "SECRET_KEY": "__TEST_SECRET__",
                "JWT_EXPIRE_DAYS": 3,
            }

            def before_request(self, t):
                pass

        app = App()
        flask_jwt_router = JwtRoutes(app)

        result = flask_jwt_router.config.secret_key
        assert result == "__TEST_SECRET__"
        assert flask_jwt_router.config.expire_days == 3
        assert flask_jwt_router.exp == 3

        class App:
            config = {
                "SECRET_KEY": "__TEST_SECRET__",
                "JWT_EXPIRE_DAYS": 99,
            }

            def before_request(self, t):
                pass

        app = App()
        flask_jwt_router_two = JwtRoutes(app)
        result_two = flask_jwt_router_two.config.secret_key
        assert result_two == "__TEST_SECRET__"
        assert flask_jwt_router_two.config.expire_days == 99
        assert flask_jwt_router_two.exp == 99

    def test_set_exp(self):
        flask_jwt_router = JwtRoutes()
        flask_jwt_router.set_exp(expire_days=10)
        assert flask_jwt_router.exp == 10
        flask_jwt_router.set_exp()
        assert flask_jwt_router.exp == 30

    def test_get_entity_id(self):

        flask_jwt_router = JwtRoutes()
        result = flask_jwt_router.get_entity_id(entity_id=1)
        assert result == 1
        result_two = flask_jwt_router.get_entity_id()
        assert result_two is None

    def test_get_app_config(self):
        white_list = [("POST", "/test")]
        class App:
            config = {
                "SECRET_KEY": "__TEST_SECRET__",
                "WHITE_LIST_ROUTES": white_list
            }
        app = App()
        flask_jwt_router = JwtRoutes()
        config = flask_jwt_router.get_app_config(app)
        assert config["WHITE_LIST_ROUTES"] == white_list

    def test_create_token(self):
        class App:
            config = {
                "SECRET_KEY": "__TEST_SECRET__"
            }
            def before_request(self, t):
                pass
        app = App()
        flask_jwt_router = JwtRoutes(app)

        with pytest.raises(KeyError, match=r"create_token.+") as excinfo:
            token = flask_jwt_router.create_token(entity_id=1)

    def test_set_expire_days(self):
        jwt = JwtRoutes()
        self.app.config["JWT_EXPIRE_DAYS"] = 99
        jwt.init_app(self.app)
        assert jwt.config.expire_days == 99
        assert jwt.exp == 99
        jwt.set_exp(expire_days=22)
        assert jwt.exp == 22

    def test_get_strategy(self):
        jwt = JwtRoutes()
        jwt.init_app(self.app, google_oauth=self.oauth_options, strategies=[GoogleTestUtil])
        strategy = jwt.get_strategy("GoogleTestUtil")
        assert isinstance(strategy, GoogleTestUtil)

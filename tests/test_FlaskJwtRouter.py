import pytest

# from flask_jwt_router.JwtRoutes import JwtRoutes
from flask_jwt_router.FlaskJwtRouter import FlaskJwtRouter

from flask_jwt_router._jwt_routes import JwtRoutes
from flask_jwt_router._entity import Entity

class TestFlaskJwtRouter:

    @pytest.mark.test
    def test_get_app_config(self):
        white_list = [("POST", "/test")]
        class App:
            config = {
                "WHITE_LIST_ROUTES": white_list
            }
        app = App()
        flask_jwt_router = JwtRoutes()
        config = flask_jwt_router.get_app_config(app)
        assert config["WHITE_LIST_ROUTES"] == white_list

    @pytest.mark.test
    def test_get_entity_id(self):

        flask_jwt_router = JwtRoutes()
        result = flask_jwt_router.get_entity_id(entity_id=1)
        assert result == 1
        result_two = flask_jwt_router.get_entity_id()
        assert result_two is None

    @pytest.mark.test
    def test_get_exp(self):
        flask_jwt_router = JwtRoutes()
        result = flask_jwt_router.get_exp(exp=10)
        assert result == 10
        result = flask_jwt_router.get_exp()
        assert result == 30

    @pytest.mark.test
    def test_get_secret_key(self):
        class App:
            config = {
                "SECRET_KEY": "123abc"
            }
            def before_request(self, t):
                pass
        app = App()
        flask_jwt_router = JwtRoutes(app)

        result = flask_jwt_router.extensions.secret_key
        assert result == "123abc"

        class App:
            config = {}
            def before_request(self, t):
                pass
        app = App()
        flask_jwt_router_two = JwtRoutes(app)
        result_two = flask_jwt_router_two.extensions.secret_key
        assert result_two == "DEFAULT_SECRET_KEY"

    @pytest.mark.test
    def test_auth_model(self):
        class AuthModel:
            pass
        result = Entity.set_entity_model({"entity_model":AuthModel})
        assert result == AuthModel

    @pytest.mark.test
    def test_config(self):
        IGNORED_ROUTES = [
            ("GET", "/"),
            ("GET", "/ignore"),
        ]
        WHITE_LIST_ROUTES = [
            ("GET", "/test"),
        ]
        class App:
            config = {
                "IGNORED_ROUTES": IGNORED_ROUTES,
                "WHITE_LIST_ROUTES": WHITE_LIST_ROUTES,
            }
            def before_request(self, t):
                pass
        flask_jwt_router = JwtRoutes(App())
        assert flask_jwt_router.extensions.ignored_routes == IGNORED_ROUTES
        assert flask_jwt_router.extensions.whitelist_routes == WHITE_LIST_ROUTES
        flask_jwt = JwtRoutes()
        flask_jwt.init_app(App())
        assert flask_jwt.extensions.ignored_routes == IGNORED_ROUTES
        assert flask_jwt.extensions.whitelist_routes == WHITE_LIST_ROUTES




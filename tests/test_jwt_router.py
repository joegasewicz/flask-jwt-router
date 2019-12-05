from flask_jwt_router._jwt_routes import JwtRoutes
import pytest

class TestJwtRouter:
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

    def test_get_exp(self):
        flask_jwt_router = JwtRoutes()
        result = flask_jwt_router.get_exp(exp=10)
        assert result == 10
        result = flask_jwt_router.get_exp()
        assert result == 30

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
                "WHITE_LIST_ROUTES": white_list
            }
        app = App()
        flask_jwt_router = JwtRoutes()
        config = flask_jwt_router.get_app_config(app)
        assert config["WHITE_LIST_ROUTES"] == white_list

    def test_register_entity(self):
        class App:
            config = {
                "SECRET_KEY": "123abc"
            }
            def before_request(self, t):
                pass
        app = App()
        flask_jwt_router = JwtRoutes(app)

        with pytest.raises(KeyError, match=r"register_entity.+") as excinfo:
            token = flask_jwt_router.register_entity(entity_id=1)

from flask_jwt_router.FlaskJwtRouter import FlaskJwtRouter

class TestFlaskJwtRouter:

    def test_get_app_config(self):
        white_list = [("POST", "/test")]
        class App:
            config = {
                "WHITE_LIST_ROUTES": white_list
            }
        app = App()
        flask_jwt_router = FlaskJwtRouter()
        config = flask_jwt_router.get_app_config(app)
        assert config["WHITE_LIST_ROUTES"] == white_list

    def test_get_entity_key(self):
        class App:
            config = {
                "ENTITY_KEY": "user_id"
            }

        app = App()
        flask_jwt_router = FlaskJwtRouter(app)
        result = flask_jwt_router.get_entity_key()
        assert result == "user_id"

        class AppTwo:
            config = {}

        app_two = AppTwo()

        flask_jwt_router_two = FlaskJwtRouter(app_two)
        result_two = flask_jwt_router_two.get_entity_key()
        assert result_two == "id"

    def test_get_entity_id(self):

        flask_jwt_router = FlaskJwtRouter()
        result = flask_jwt_router.get_entity_id(entity_id=1)
        assert result == 1
        result_two = flask_jwt_router.get_entity_id()
        assert result_two is None

    def test_get_exp(self):
        flask_jwt_router = FlaskJwtRouter()
        result = flask_jwt_router.get_exp(exp=10)
        assert result == 10
        result = flask_jwt_router.get_exp()
        assert result == 30

    def test_get_secret_key(self):
        class App:
            config = {
                "SECRET_KEY": "123abc"
            }
        app = App()
        flask_jwt_router = FlaskJwtRouter(app)
        result = flask_jwt_router.get_secret_key()
        assert result == "123abc"

        class App:
            config = {}
        app = App()
        flask_jwt_router_two = FlaskJwtRouter(app)
        result_two = flask_jwt_router_two.get_secret_key()
        assert result_two == "DEFAULT_SECRET_KEY"

    def test_auth_model(self):
        class AuthModel:
            pass
        result = FlaskJwtRouter.set_entity_model({"entity_model":AuthModel})
        assert result == AuthModel

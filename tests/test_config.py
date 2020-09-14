from flask_jwt_router._jwt_routes import JwtRoutes
from flask_jwt_router._config import Config
from tests.fixtures.model_fixtures import MockEntityModel


class TestConfig:
    IGNORED_ROUTES = [
        ("GET", "/"),
        ("GET", "/ignore"),
    ]
    WHITE_LIST_ROUTES = [
        ("GET", "/test"),
    ]

    config = {
                "IGNORED_ROUTES": IGNORED_ROUTES,
                "WHITE_LIST_ROUTES": WHITE_LIST_ROUTES,
                "SECRET_KEY": "a sectrect key",
                "JWT_ROUTER_API_NAME": "api/v1",
                "ENTITY_KEY": "user_id",
                "JWT_EXPIRE_DAYS": 6,
            }

    def test_init_config(self, MockEntityModel):
        config = Config()
        config.init_config(self.config, entity_models=[MockEntityModel])

        assert config.whitelist_routes == self.WHITE_LIST_ROUTES
        assert config.ignored_routes == self.IGNORED_ROUTES
        assert config.entity_models == [MockEntityModel]
        assert config.entity_key == "user_id"
        assert config.api_name == "api/v1"
        assert config.expire_days == 6

        config_two = {**self.config, "ENTITY_MODELS": [MockEntityModel]}
        config.init_config(config_two)

        assert config.entity_models == [MockEntityModel]
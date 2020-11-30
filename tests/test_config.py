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

    oauth_options = {
        "client_id": "<CLIENT_ID>",
        "client_secret": "<CLIENT_SECRET>",
        "redirect_uri": "http://localhost:3000",
        "tablename": "users",
        "email_field": "email",
        "expires_in": 3600,
    }

    def test_init_config(self, MockEntityModel):
        config = Config()

        config.init_config(
            self.config,
            entity_models=[MockEntityModel],
            google_oauth=self.oauth_options,
        )

        assert config.whitelist_routes == self.WHITE_LIST_ROUTES
        assert config.ignored_routes == self.IGNORED_ROUTES
        assert config.entity_models == [MockEntityModel]
        assert config.entity_key == "user_id"
        assert config.api_name == "api/v1"
        assert config.expire_days == 6
        assert hasattr(config, "oauth_entity")
        assert hasattr(config, "oauth_entity")
        assert config.google_oauth["client_id"] == "<CLIENT_ID>"
        assert config.google_oauth["client_secret"] == "<CLIENT_SECRET>"
        assert config.google_oauth["redirect_uri"] == "http://localhost:3000"
        assert config.google_oauth["tablename"] == "users"
        assert config.google_oauth["email_field"] == "email"
        assert config.google_oauth["expires_in"] == 3600

        config_two = {**self.config, "ENTITY_MODELS": [MockEntityModel]}
        config.init_config(config_two)

        assert config.entity_models == [MockEntityModel]


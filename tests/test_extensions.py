from flask_jwt_router._jwt_routes import JwtRoutes
from flask_jwt_router._extensions import Extensions
from tests.fixtures.model_fixtures import MockEntityModel


class TestExtension:
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
            }

    def test_init_extensions(self, MockEntityModel):
        extensions = Extensions()
        config = extensions.init_extensions(self.config, entity_models=[MockEntityModel])

        assert config.whitelist_routes == self.WHITE_LIST_ROUTES
        assert config.ignored_routes == self.IGNORED_ROUTES
        assert config.entity_models == [MockEntityModel]
        assert config.entity_key == "user_id"
        assert config.api_name == "api/v1"

        config = {**self.config, "ENTITY_MODELS": [MockEntityModel]}
        con = extensions.init_extensions(config)

        assert con.entity_models == [MockEntityModel]


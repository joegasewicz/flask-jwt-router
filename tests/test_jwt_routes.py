from flask import Flask


from flask_jwt_router._jwt_routes import JwtRoutes
from tests.fixtures.model_fixtures import MockEntityModel


class TestJwtRoutes:

    app = Flask(__name__)

    def test_init_app(self):
        jwt = JwtRoutes(self.app, entity_models=[MockEntityModel])
        assert jwt.extensions.entity_models[0] == MockEntityModel
        assert jwt.app == self.app

        jwt = JwtRoutes()
        jwt.init_app(self.app, entity_models=[MockEntityModel])
        assert jwt.extensions.entity_models[0] == MockEntityModel
        assert jwt.app == self.app

        jwt = JwtRoutes(self.app)
        jwt.init_app(entity_models=[MockEntityModel])
        assert jwt.extensions.entity_models[0] == MockEntityModel
        assert jwt.app == self.app

        jwt = JwtRoutes(entity_models=[MockEntityModel])
        jwt.init_app(self.app)
        assert jwt.extensions.entity_models[0] == MockEntityModel
        assert jwt.app == self.app

        self.app.config["ENTITY_MODELS"] = [MockEntityModel]
        jwt = JwtRoutes()
        jwt.init_app(self.app)
        assert jwt.extensions.entity_models[0] == MockEntityModel
        assert jwt.app == self.app

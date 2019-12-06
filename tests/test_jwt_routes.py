from flask import Flask


from flask_jwt_router._jwt_routes import JwtRoutes
from tests.fixtures.model_fixtures import MockEntityModel


class TestJwtRoutes:

    app = Flask(__name__)
    jwt_routes = JwtRoutes(app)

    def test_create_token_from_model(self, MockEntityModel):
        token = self.jwt_routes.create_token_from_model(MockEntityModel)
        assert isinstance(token, str)


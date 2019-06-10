import pytest

from flask_jwt_router.JwtRoutes import JwtRoutes
from tests.fixtures import jwt_router_client

class UserModel:
    id = 1

class TestJwtRoutes:

    @pytest.mark.parametrize(
        "jwt_router_client,entity_model,expected", [
            ({"WHITE_LIST_ROUTES": [("GET", "/test")]}, None, "200"),
            ({"WHITE_LIST_ROUTES": []}, None, "401"),
            ({"WHITE_LIST_ROUTES": [("POST", "/test")]}, None, "401"),
        ], indirect=["jwt_router_client"]
    )
    def test_jwt_route(self, jwt_router_client, entity_model, expected):
        rv = jwt_router_client.get("/test")
        assert expected in str(rv.status)


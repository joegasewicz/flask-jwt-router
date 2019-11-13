import pytest
from flask_jwt_router.JwtRoutes import JwtRoutes

from flask_jwt_router.JwtRoutes import JwtRoutes
from tests.fixtures import jwt_router_client, test_client, test_client_static


class UserModel:
    id = 1


class TestJwtRoutes:

    @pytest.mark.parametrize(
        "jwt_router_client,entity_model,expected", [
            ({"WHITE_LIST_ROUTES": [("GET", "/test")]}, None, "200"),
            ({"WHITE_LIST_ROUTES": []}, None, "401"),
            ({"WHITE_LIST_ROUTES": [("POST", "/test")]}, None, "401"),
            ({}, None, "401"),
        ], indirect=["jwt_router_client"]
    )
    def test_jwt_route(self, jwt_router_client, entity_model, expected):
        rv = jwt_router_client.get("/test")
        assert expected in str(rv.status)

    def test_api_named_routes(self, test_client):
        rv = test_client.get("/api/v1/test")
        assert "200" in str(rv.status)

    def test_sub_paths(self, test_client):
        rv = test_client.get("/api/v1/bananas/sub")
        assert "200" in str(rv.status)
        assert rv.get_json()["data"] == "sub"

        rv = test_client.get("/api/v1/test/sub_two")
        assert "401" in str(rv.status)

    def test_dynamic_params(self, test_client):
        rv = test_client.put("/api/v1/apples/sub/1")
        assert "200" in str(rv.status)

        rv = test_client.get("/api/v1/apples/sub/")
        assert "401" in str(rv.status)

        rv = test_client.get("/api/v1/apples/sub/hello")
        assert "401" in str(rv.status)

    def test_static_routes(self, test_client, test_client_static):
        """
        Tests if the static path is handled both by default and
        if the path is past to the static_folder kwarg
        """
        rv = test_client.get("/static/images/Group.jpg")
        assert "200" in str(rv.status)

        rv = test_client_static.get("/static_copy/images/Group.jpg")
        assert "200" in str(rv.status)



"""
    Unit Tests for:
        - Routing class: that deal with encoding & decoding tokens & authorising routes.
        - Entity class: This covers the get_id_from_token method.

    Extension values used in routing:

    "WHITE_LIST_ROUTES" = [("PUT", "/banana")]
    "IGNORED_ROUTES" = [("GET", "/")]
    "JWT_ROUTER_API_NAME" = "/api/v1"
"""
from flask import Flask
from typing import Any
import pytest

from flask_jwt_router._routing import Routing
from flask_jwt_router._extensions import Extensions
from flask_jwt_router._entity import Entity
from tests.fixtures.token_fixture import mock_token
from tests.fixtures.model_fixtures import TestMockEntity
from tests.fixtures.app_fixtures import jwt_router_client, test_client_static
from tests.fixtures.main_fixture import test_client


class MockArgs:
    def __init__(self, token=None, headers=False):
        self.token = token
        self.headers = headers

    def get(self, t):
        if self.headers:
            return f"Bearer {self.token}"
        else:
            return self.token


class TestRouting:

    app = None
    extensions = {
        "WHITE_LIST_ROUTES": [("PUT", "/banana")],
        "IGNORED_ROUTES": [("GET", "/")],
        "JWT_ROUTER_API_NAME": "/api/v1",
        "SECRET_KEY": "TEST_SECRET",
    }
    ext = Extensions().init_extensions(extensions)

    def test_before_middleware(self, monkeypatch, TestMockEntity, mock_token):
        app = Flask(__name__)
        # Manually set the primary key
        entity = TestMockEntity(id=1, user_name="joe")

        ctx = app.test_request_context("/test")
        ctx.push()

        assert entity.user_name == "joe"
        assert entity.id == 1

        self.ext.entity_models = [TestMockEntity]
        entity = Entity(self.ext)
        routing = Routing(app, self.ext, entity)

        with ctx:
            # token from args
            monkeypatch.setattr("flask.request.args", MockArgs(mock_token))
            routing.before_middleware()
            assert ctx.g.test_entities == [(1, 'joe')]

        with ctx:
            # token from headers
            monkeypatch.setattr("flask.request.args", MockArgs())
            monkeypatch.setattr("flask.request.headers", MockArgs(mock_token, True))
            routing.before_middleware()
            assert ctx.g.test_entities == [(1, 'joe')]

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

    def test_static_routes(self, test_client):
        """
        Tests if the static path is handled both by default and
        if the path is past to the static_folder kwarg
        """
        rv = test_client.get("/static/images/Group.jpg")
        assert "200" in str(rv.status)

        rv = test_client.get("/")
        assert "200" in str(rv.status)

    def test_static_client(self, test_client_static):
        rv = test_client_static.get("/static_copy/images/Group.jpg")
        assert "200" in str(rv.status)

    def test_ignored_routes(self, test_client):
        rv = test_client.get("/ignore")
        assert "200" in str(rv.status)

    def test_ignored_route_path(self, test_client):
        rv = test_client.get("/")
        assert "200" in str(rv.status)




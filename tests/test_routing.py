"""
    Tests for Routing class that deal with encoding & decoding
    tokens & authorising routes.

    Extension values used in routing:

    "WHITE_LIST_ROUTES" = [("PUT", "/banana")]
    "IGNORED_ROUTES" = [("GET", "/")]
    "JWT_ROUTER_API_NAME" = "/api/v1"
"""
from flask import Flask
from typing import Any

from flask_jwt_router._routing import Routing
from flask_jwt_router._extensions import Extensions
from .token_fixture import mock_token
from .model_fixtures import TestEntity


class GlobalEntity:
    _entity: Any

    def __init__(self):
        self._entity = None

    @property
    def entity(self):
        return self._entity

    @entity.setter
    def entity(self, value):
        self._entity = value


class MockArgs:
    def __init__(self, token=None):
        self.token = token

    def get(self, t):
        return self.token
#  TODO    "Authorization": f"Bearer {self.token}",


class TestRouting:

    app = None
    extensions = {
        "WHITE_LIST_ROUTES": [("PUT", "/banana")],
        "IGNORED_ROUTES": [("GET", "/")],
        "JWT_ROUTER_API_NAME": "/api/v1",
        "SECRET_KEY": "TEST_SECRET",
    }
    ext = Extensions().init_extensions(extensions)

    def test_before_middleware(self, monkeypatch, TestEntity, mock_token):
        app = Flask(__name__)
        # Manually set the primary key
        entity = TestEntity(id=1, user_name="joe")
        assert entity.user_name == "joe"
        assert entity.id == 1

        ctx = app.test_request_context("/test")
        ctx.push()
        _g = GlobalEntity()

        with ctx:
            monkeypatch.setattr("flask.request.args", MockArgs(mock_token))
            monkeypatch.setattr("flask.request.headers", MockArgs(mock_token))
            # monkeypatch.setattr("flask.g", _g)

            routing = Routing(app, self.ext, entity)

            assert routing.extensions

            routing.before_middleware()
            assert ctx.g.entity == 1

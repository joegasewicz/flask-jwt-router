"""
    The purpose of this module is to test the Entity class
    can decode & encode JSON web tokens correctly & return
    an entity's data.

    The extension variables used in this class are:
        - SECRET_KEY or __TEST_SECRET__
        - ENTITY_KEY or id

    Start with a decoded token (as the Router class handles this):


"""
import pytest
import jwt
from flask import jsonify

from flask_jwt_router._entity import Entity
from flask_jwt_router._extensions import Extensions
from flask_jwt_router._routing import Routing
from tests.fixtures.main_fixture import test_client, jwt_routes
from tests.fixtures.token_fixture import mock_decoded_token, mock_decoded_token_two, mock_decoded_token_three
from tests.fixtures.model_fixtures import MockEntityModel, NoTableNameEntity, MockEntityModelTwo, MockEntityModelThree
from tests.fixtures.models import TeacherModel


class MockArgs:
    def __init__(self, token=None, headers=False):
        self.token = token
        self.headers = headers

    def get(self, t):
        if self.headers:
            return f"Bearer {self.token}"
        else:
            return self.token


class TestEntity:
    """
        Entity class public methods tests
    """
    extensions = {
        "WHITE_LIST_ROUTES": [("PUT", "/banana")],
        "IGNORED_ROUTES": [("GET", "/")],
        "JWT_ROUTER_API_NAME": "/api/v1",
        "SECRET_KEY": "__TEST_SECRET__",
        "ENTITY_KEY": "id",
    }
    ext = Extensions().init_extensions(extensions)

    token_non_entity = {'id': 12, 'exp': 1577037162}

    def test_get_entity_from_token(self, MockEntityModelThree, mock_decoded_token_three):

        self.ext.entity_models = [MockEntityModelThree]

        entity = Entity(self.ext)

        assert entity.get_entity_from_token(mock_decoded_token_three) == [(1, 'joe')]

    def test_get_entity_from_token_multiple(self, MockEntityModel, MockEntityModelTwo, mock_decoded_token_two):

        self.ext.entity_models = [MockEntityModel, MockEntityModelTwo]

        entity = Entity(self.ext)

        assert entity.get_entity_from_token(mock_decoded_token_two) == [(1, 'joe')]

    def test_get_attr_name(self, MockEntityModel, mock_decoded_token):

        self.ext.entity_models = [MockEntityModel]

        entity = Entity(self.ext)
        entity.get_entity_from_token(mock_decoded_token)

        result = entity.get_attr_name()

        assert result == "id"

    def test_get_attr_name(self, test_client):
        rv = test_client.post("/api/v1/test_entity")
        assert "200" in str(rv.status)
        assert "token" in str(rv.get_json())

        token = rv.get_json()["token"]

        decoded_token = jwt.decode(
                token,
                "__TEST_SECRET__",
                algorithms="HS256"
            )

        assert decoded_token["table_name"] == "teachers"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        rv_get = test_client.get("/api/v1/test_entity", headers=headers)

        assert "200" in str(rv_get.status)
        assert "token" in str(rv_get.get_json())
        assert rv_get.get_json()["data"] == {"teacher_id": 1, "name": "joe"}

        token_two = rv_get.get_json()["token"]

        decoded_token_two = jwt.decode(
                token_two,
                "__TEST_SECRET__",
                algorithms="HS256"
            )

        assert decoded_token_two["table_name"] == "teachers"


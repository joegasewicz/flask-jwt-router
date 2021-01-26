"""
    The purpose of this module is to test the Entity class
    can decode & encode JSON web tokens correctly & return
    an entity's data.

    The configension variables used in this class are:
        - SECRET_KEY or __TEST_SECRET__
        - ENTITY_KEY or id

    Start with a decoded token (as the Router class handles this):


"""
import pytest
import jwt
from flask import jsonify

from flask_jwt_router._entity import Entity
from flask_jwt_router._config import Config
from flask_jwt_router._routing import Routing
from tests.fixtures.main_fixture import request_client, jwt_routes
from tests.fixtures.token_fixture import (
    mock_decoded_token,
    mock_decoded_token_two,
    mock_decoded_token_three,
)
from tests.fixtures.model_fixtures import (
    MockEntityModel,
    NoTableNameEntity,
    MockEntityModelTwo,
    MockEntityModelThree,
    MockAOuthModel,
)

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
    app_config = {
        "WHITE_LIST_ROUTES": [("PUT", "/banana")],
        "IGNORED_ROUTES": [("GET", "/")],
        "JWT_ROUTER_API_NAME": "/api/v1",
        "SECRET_KEY": "__TEST_SECRET__",
        "ENTITY_KEY": "id",
    }
    oauth_options = {
        "client_id": "<CLIENT_ID>",
        "client_secret": "<CLIENT_SECRET>",
        "redirect_uri": "http://localhost:3000",
        "tablename": "users",
        "email_field": "email",
        "expires_in": 3600,
    }
    config = Config()
    config.init_config(app_config)

    token_non_entity = {'id': 12, 'exp': 1577037162}

    def test_get_entity_from_token_or_tablename(self, MockEntityModelThree, mock_decoded_token_three, MockAOuthModel):

        self.config.entity_models = [MockEntityModelThree]
        entity = Entity(self.config)
        assert entity.get_entity_from_token_or_tablename(mock_decoded_token_three) == [(1, 'joe')]

        self.config.entity_models = [MockAOuthModel]
        self.config.google_oauth = self.oauth_options
        entity = Entity(self.config)
        entity.oauth_entity_key = "email"
        assert entity.get_entity_from_token_or_tablename(tablename="oauth_tablename") == [(1, 'joe')]

    def test_get_entity_from_token_multiple(self, MockEntityModel, MockEntityModelTwo, MockAOuthModel, mock_decoded_token_two):

        self.config.entity_models = [MockEntityModel, MockAOuthModel, MockEntityModelTwo]
        entity = Entity(self.config)
        assert entity.get_entity_from_token_or_tablename(mock_decoded_token_two) == [(1, 'joe')]

        self.config.entity_models = [MockEntityModel, MockAOuthModel, MockEntityModelTwo]
        self.config.google_oauth = self.oauth_options
        entity = Entity(self.config)
        entity.oauth_entity_key = "email"
        assert entity.get_entity_from_token_or_tablename(tablename="oauth_tablename") == [(1, 'joe')]

    def test_get_attr_name(self, MockEntityModel, mock_decoded_token):

        self.config.entity_models = [MockEntityModel]

        entity = Entity(self.config)
        entity.get_entity_from_token_or_tablename(mock_decoded_token)

        result = entity.get_attr_name()

        assert result == "id"

    @pytest.mark.skip
    def test_get_attr_name(self, request_client):
        from tests.fixtures.models import TeacherModel
        from tests.fixtures.main_fixture import db
        teacher = TeacherModel(name="joe")
        db.session.add(teacher)
        db.session.commit()
        rv = request_client.post("/api/v1/test_entity")
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
        rv_get = request_client.get("/api/v1/test_entity", headers=headers)

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


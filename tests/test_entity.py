"""
    The purpose of this module is to test the Entity class
    can decode & encode JSON web tokens correctly & return
    an entity's data.

    The extension variables used in this class are:
        - SECRET_KEY or DEFAULT_SECRET_KEY
        - ENTITY_KEY or id

    Start with a decoded token (as the Router class handles this):


"""
import pytest

from flask_jwt_router._entity import Entity
from flask_jwt_router._extensions import Extensions
from tests.fixtures.token_fixture import mock_decoded_token
from tests.fixtures.model_fixtures import MockEntityModel


class TestEntity:
    """
        Entity class public methods tests
    """
    extensions = {
        "WHITE_LIST_ROUTES": [("PUT", "/banana")],
        "IGNORED_ROUTES": [("GET", "/")],
        "JWT_ROUTER_API_NAME": "/api/v1",
        "SECRET_KEY": "TEST_SECRET",
        "ENTITY_KEY": "id",
    }
    ext = Extensions().init_extensions(extensions)

    token_non_entity = {'id': 12, 'exp': 1577037162}

    def test_get_id_from_token(self, MockEntityModel, mock_decoded_token):

        self.ext.entity_models = [MockEntityModel]

        entity = Entity(self.ext)

        assert self.ext.entity_key == "id"
        assert entity.get_entity_from_token(mock_decoded_token) == [(1, 'joe')]

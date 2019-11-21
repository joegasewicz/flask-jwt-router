"""
    The purpose of this module is to test the Entity class
    can decode & encode JSON web tokens correctly & return
    an entity's data.

    The extension variables used in this class are:
        - SECRET_KEY or DEFAULT_SECRET_KEY
        - ENTITY_KEY or id

    Start with a decoded token (as the Router class handles this):


"""
from flask_jwt_router._entity import Entity


class MockModel:
    pass


class TestEntity:
    """
        Entity class public methods tests
    """
    mock_extensions = {
        "SECRET_KEY": "DEFAULT_SECRET_KEY",
        "ENTITY_KEY": "id",
    }
    mock_auth = MockModel()
    mock_token = ""

    def test_get_id_from_token(self):
        entity = Entity(self.mock_extensions, self.mock_auth)


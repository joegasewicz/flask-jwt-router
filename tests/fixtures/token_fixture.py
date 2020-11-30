import jwt
import pytest
from datetime import datetime
from dateutil.relativedelta import *


new_token = jwt.encode({
            "table_name": "test_entities",
            "id": 1,
            "exp": datetime.utcnow() + relativedelta(days=+30)
        },
            "__TEST_SECRET__",
            algorithm="HS256"
        ).decode("utf-8")


@pytest.fixture
def mock_token():
    return new_token


@pytest.fixture
def mock_access_token():
    return "Bearer <ACCESS_TOKEN>"


@pytest.fixture
def mock_decoded_token():
    return jwt.decode(
            new_token,
            "__TEST_SECRET__",
            algorithms="HS256"
    )


new_token_two = jwt.encode({
            "table_name": "test_two_entities",
            "id": 1,
            "exp": datetime.utcnow() + relativedelta(days=+30)
        },
            "__TEST_SECRET__",
            algorithm="HS256"
        ).decode("utf-8")


@pytest.fixture
def mock_token_two():
    return new_token_two


@pytest.fixture
def mock_decoded_token_two():
    return jwt.decode(
            new_token_two,
            "__TEST_SECRET__",
            algorithms="HS256"
    )


new_token_three = jwt.encode({
            "table_name": "test_3_entities",
            "teacher_id": 1,
            "exp": datetime.utcnow() + relativedelta(days=+30)
        },
            "__TEST_SECRET__",
            algorithm="HS256"
        ).decode("utf-8")


@pytest.fixture
def mock_token_three():
    return new_token_three


@pytest.fixture
def mock_decoded_token_three():
    return jwt.decode(
            new_token_three,
            "__TEST_SECRET__",
            algorithms="HS256"
    )


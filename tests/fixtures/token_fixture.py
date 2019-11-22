import jwt
import pytest
from datetime import datetime
from dateutil.relativedelta import *


new_token = jwt.encode({
            "id": 1,
            "exp": datetime.utcnow() + relativedelta(days=+30)
        },
            "TEST_SECRET",
            algorithm="HS256"
        ).decode("utf-8")


@pytest.fixture
def mock_token():
    return new_token


@pytest.fixture
def mock_decoded_token():
    return jwt.decode(
            new_token,
            "TEST_SECRET",
            algorithms="HS256"
    )

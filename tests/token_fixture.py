import jwt
import pytest
from datetime import datetime
from dateutil.relativedelta import *


@pytest.fixture
def mock_token():
    return jwt.encode({
            "id": 1,
            "exp": datetime.utcnow() + relativedelta(days=+30)
        },
            "TEST_SECRET",
            algorithm="HS256"
        ).decode("utf-8")




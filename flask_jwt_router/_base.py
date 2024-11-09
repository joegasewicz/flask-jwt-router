from abc import ABC, abstractmethod
from typing import Any
from datetime import datetime
# pylint:disable=wildcard-import,unused-wildcard-import
from dateutil.relativedelta import *
import jwt
from flask import g

from ._config import Config

class BaseAuthentication(ABC):
    # pylint:disable=missing-class-docstring
    @abstractmethod
    def create_token(self, config: Config, exp: int, **kwargs):
        # pylint:disable=missing-function-docstring
        pass

    @abstractmethod
    def update_token(self, config: Config, exp: int, table_name, **kwarg):
        # pylint:disable=missing-function-docstring
        pass

    @abstractmethod
    def encode_token(self, config: Config, entity_id: Any, exp: int, table_name: str):
        # pylint:disable=missing-function-docstring
        pass


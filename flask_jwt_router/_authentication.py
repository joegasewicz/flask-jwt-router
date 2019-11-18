"""
    AuthStrategy class are strategies with public methods
    defined in BaseAuthStrategy. Currently only 2 of the
    3 methods are used publicly but the intention is there...

    Example with different cryptographic signing Algorithm:

    class AnotherAuthStrategy(BaseAuthStrategy):
    def encode_token(self, extensions: Config, **kwargs):
        pass

    def register_entity(self):
        pass

    def update_entity(self):
        pass

"""
from abc import ABC, abstractmethod
import jwt
from typing import Any
from datetime import datetime
from dateutil.relativedelta import *

from ._extensions import Config


class BaseAuthStrategy(ABC):

    @abstractmethod
    def register_entity(self, extensions: Config, exp: Any, **kwargs):
        pass

    @abstractmethod
    def update_entity(self, extensions: Config, exp: Any, **kwargs):
        pass

    def encode_token(self, extensions: Config, entity_id: Any, exp: Any):
        pass


class JWTAuthStrategy(BaseAuthStrategy):
    """
        Uses SHA-256 hash algorithm
    """

    def __init__(self):
        super(JWTAuthStrategy, self).__init__()

    def encode_token(self, extensions: Config, entity_id: Any, exp: Any):
        """
        :param extensions:
        :param entity_id:
        :param exp:
        :return:
        """
        entity_key = extensions.entity_key
        secret_key = extensions.secret_key

        encoded = jwt.encode({
            entity_key: entity_id,
            "exp": datetime.utcnow() + relativedelta(days=+exp)  # TODO options for different time types
        },
            secret_key,
            algorithm="HS256"
        ).decode("utf-8")
        return encoded

    def register_entity(self, extensions: Config, exp: Any, **kwargs):
        """
        :param extensions:
        :param exp:
        :param kwargs:
        :return:
        """
        entity_id = kwargs.get("entity_id", None)
        if entity_id:
            token = self.encode_token(extensions, exp, entity_id)
            return token
        else:
            return None

    def update_entity(self, extensions: Config, exp: Any, **kwargs):
        """
        :param extensions:
        :param exp:
        :param kwargs:
        :return:
        """
        entity_id = kwargs.get("entity_id", None)
        if entity_id:
            token = self.encode_token(extensions, exp, entity_id)
            return token
        else:
            return None



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
from datetime import datetime
from dateutil.relativedelta import *

from ._extensions import Config
from ._entity import Entity


class _AuthUtility:
    @staticmethod
    def get_exp(**kwargs):
        """
        :param kwargs: Dict[str, int]
        :return: number
        """
        try:
            return kwargs['exp']
        except KeyError as _:
            return 30


class BaseAuthStrategy(ABC):

    @abstractmethod
    def register_entity(self, **kwargs):
        pass

    @abstractmethod
    def update_entity(self, **kwargs):
        pass

    @abstractmethod
    def encode_token(self, extensions: Config, **kwargs):
        pass


class JWTAuthStrategy(BaseAuthStrategy):
    """
        Uses SHA-256 hash algorithm
    """

    def __init__(self):
        super(JWTAuthStrategy, self).__init__()

    def encode_token(self, extensions: Config, **kwargs):
        """
        :param extensions:
        :param kwargs:
        :return:
        """
        entity_key = extensions.entity_key

        exp = _AuthUtility.get_exp(**kwargs)

        secret_key = extensions.secret_key

        if Entity.get_entity_id(**kwargs):
            entity_id = Entity.get_entity_id(**kwargs)
        else:
            raise KeyError("Entity id not in kwargs")

        encoded = jwt.encode({
            entity_key: entity_id,
            "exp": datetime.utcnow() + relativedelta(days=+exp)  # TODO options for different time types
        },
            secret_key,
            algorithm="HS256"
        ).decode("utf-8")
        return encoded

    def register_entity(self, **kwargs):
        """
        :param kwargs:
        :return: str
        """
        return JWTAuthStrategy.encode_token(**kwargs)

    def update_entity(self, **kwargs):  # TODO remove, duplicate method!
        """
        :param kwargs:
        :return: str
        """
        return JWTAuthStrategy.encode_token(**kwargs)


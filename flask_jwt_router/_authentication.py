"""
    AuthStrategy class are strategies with public methods
    defined in BaseAuthStrategy. Currently only 2 of the
    3 methods are used publicly but the intention is there...
"""
from abc import ABC, abstractmethod
import jwt
from datetime import datetime
from dateutil.relativedelta import *

from flask_jwt_router._extensions import _Extensions
from flask_jwt_router._entity import BaseEntity


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
    def register_entity(self):
        pass

    @abstractmethod
    def update_entity(self):
        pass

    @staticmethod
    @abstractmethod
    def encode_token(extensions: _Extensions, **kwargs):
        pass


class JWTAuthStrategy(BaseAuthStrategy):

    def __init__(self, entity: BaseEntity):
        super(JWTAuthStrategy, self).__init__()

        self.entity = entity

    def encode_token(self, extensions: _Extensions, **kwargs):
        """
        :param extensions:
        :param kwargs:
        :return:
        """
        entity_key = extensions.entity_key

        exp = _AuthUtility.get_exp(**kwargs)

        secret_key = extensions.secret_key

        if self.entity.get_entity_id(**kwargs):
            entity_id = self.entity.get_entity_id(**kwargs)
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


class SSHAuthStrategy(BaseAuthStrategy):
    def register_entity(self):
        pass

    def update_entity(self):
        pass

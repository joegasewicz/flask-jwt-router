"""
    AuthStrategy class are algorithms with public methods
    defined in BaseAuthStrategy. Currently only 2 of the
    3 methods are used publicly but the intention is there...

    Example of a new algorithm with different cryptographic signing "Algorithm"::

        class AnotherAuthStrategy(BaseAuthStrategy):
            def encode_token(self, extensions: Config, **kwargs):
                pass

            def register_entity(self):
                pass

            def update_entity(self):
                pass

"""
from abc import ABC, abstractmethod
from typing import Any, List, Tuple
from datetime import datetime
# pylint:disable=wildcard-import,unused-wildcard-import
from dateutil.relativedelta import *
import jwt

from ._extensions import Config

_ORMType = type(List[Tuple[int, str]])


class BaseAuthStrategy(ABC):
    # pylint:disable=missing-class-docstring
    @abstractmethod
    def register_entity(self, extensions: Config, exp: int, **kwargs):
        # pylint:disable=missing-function-docstring
        pass

    @abstractmethod
    def update_entity(self, extensions: Config, exp: int, entity_type, **kwarg):
        # pylint:disable=missing-function-docstring
        pass

    @abstractmethod
    def encode_token(self, extensions: Config, entity_id: Any, exp: int, entity_type: str):
        # pylint:disable=missing-function-docstring
        pass

    @abstractmethod
    def create_token_from_model(self, model: _ORMType) -> str:
        # pylint:disable=missing-function-docstring
        pass


class JWTAuthStrategy(BaseAuthStrategy):
    """
        Uses SHA-256 hash algorithm
    """
    #: The reference to the entity key. Defaulted to `id`.
    # See :class:`~flask_jwt_router._extensions` for more information.
    entity_key: str = "id"

    #: The reference to the entity key. Defaulted to `DEFAULT_SECRET_KEY`.
    #: See :class:`~flask_jwt_router._extensions` for more information.
    secret_key: str = "DEFAULT_SECRET_KEY"

    #: The reference to the entity ID.
    entity_id: str = None

    def __init__(self):
        # pylint:disable=useless-super-delegation
        super(JWTAuthStrategy, self).__init__()

    def encode_token(self, extensions: Config, entity_id: Any, exp: int, entity_type) -> str:
        """
        :param extensions: See :class:`~flask_jwt_router._extensions`
        :param entity_id: Normally the primary key `id` or `user_id`
        :param exp: The expiry duration set when encoding a new token
        :param entity_type: The Model Entity `__tablename__`
        :return: str
        """
        self.entity_key = extensions.entity_key
        self.secret_key = extensions.secret_key
        # pylint: disable=line-too-long
        encoded = jwt.encode({
            "entity_type": entity_type,
            self.entity_key: entity_id,
            # pylint: disable=no-member
            "exp": datetime.utcnow() + relativedelta(days=+exp)
        }, self.secret_key, algorithm="HS256").decode("utf-8")
        return encoded

    def register_entity(self, extensions: Config, exp: int, **kwargs) -> str:
        """
        kwargs:
            - entity_id: Represents the entity's primary key
            - entity_type: The table name of the entity
        :param extensions: See :class:`~flask_jwt_router._extensions`
        :param exp: The expiry duration set when encoding a new token
        :param kwargs:
        :return: Union[str, None]
        """
        self.entity_id = kwargs.get("entity_id", None)
        entity_type = kwargs.get("entity_type", None)
        return self.encode_token(extensions, self.entity_id, exp, entity_type)

    def update_entity(self,
                      extensions: Config,
                      exp: int,
                      entity_type: str,
                      **kwargs,
                      ) -> str:
        """
        :param extensions:
        :param exp:
        :param entity_type:
        :param kwargs:
        :return: Union[str, None]
        """
        self.entity_id = kwargs.get("entity_id", None)
        return self.encode_token(extensions, self.entity_id, exp, entity_type)

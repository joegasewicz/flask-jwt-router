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
import jwt
from typing import Any, Union
from datetime import datetime
from dateutil.relativedelta import *

from ._extensions import Config


class BaseAuthStrategy(ABC):

    @abstractmethod
    def register_entity(self, extensions: Config, exp: int, **kwargs):
        pass

    @abstractmethod
    def update_entity(self, extensions: Config, exp: int, **kwargs):
        pass

    def encode_token(self, extensions: Config, entity_id: Any, exp: int, entity_type: str):
        pass


class JWTAuthStrategy(BaseAuthStrategy):
    """
        Uses SHA-256 hash algorithm
    """
    #: The reference to the entity key. Defaulted to `id`.  See :class:`~flask_jwt_router._extensions`
    #: for more information.
    entity_key: str = "id"

    #: The reference to the entity key. Defaulted to `DEFAULT_SECRET_KEY`.
    #: See :class:`~flask_jwt_router._extensions` for more information.
    secret_key: str = "DEFAULT_SECRET_KEY"

    #: The reference to the entity ID.
    entity_id: str = None

    def __init__(self):
        super(JWTAuthStrategy, self).__init__()

    def encode_token(self, extensions: Config, entity_id: Any, exp: int, entity_type: str) -> str:
        """
        :param extensions: See :class:`~flask_jwt_router._extensions`
        :param entity_id: Normally the primary key `id` or `user_id`
        :param exp: The expiry duration set when encoding a new token
        :param entity_type: The Model Entity `__tablename__`
        :return: str
        """
        self.entity_key = extensions.entity_key
        self.secret_key = extensions.secret_key

        encoded = jwt.encode({
            "entity_type": entity_type,
            self.entity_key: entity_id,
            "exp": datetime.utcnow() + relativedelta(days=+exp)  # TODO options for different time types
        },
            self.secret_key,
            algorithm="HS256"
        ).decode("utf-8")
        return encoded

    def register_entity(self, extensions: Config, exp: int, **kwargs) -> Union[str, None]:
        """
        :param extensions: See :class:`~flask_jwt_router._extensions`
        :param exp: The expiry duration set when encoding a new token
        :param kwargs: Gets entity_id
        :return: Union[str, None]
        """
        self.entity_id = kwargs.get("entity_id", None)
        entity_type = kwargs.get("entity_type", None)
        if self.entity_id:
            token = self.encode_token(extensions, self.entity_id, exp, entity_type)
            return token
        else:
            return None

    def update_entity(self, extensions: Config, exp: int, **kwargs) -> Union[str, None]:
        """
        :param extensions:
        :param exp:
        :param kwargs:
        :return: Union[str, None]
        """
        self.entity_id = kwargs.get("entity_id", None)
        if self.entity_id:
            token = self.encode_token(extensions, self.entity_id, exp)
            return token
        else:
            return None



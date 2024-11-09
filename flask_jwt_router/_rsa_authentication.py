from abc import ABC, abstractmethod
from typing import Any
from datetime import datetime
# pylint:disable=wildcard-import,unused-wildcard-import
from dateutil.relativedelta import *
import jwt
from flask import g

from flask_jwt_router._config import Config
from flask_jwt_router._base import BaseAuthentication


class RSAAuthentication(BaseAuthentication):
    """
        Uses RSA-256 hash algorithm
    """
    #: The reference to the entity key. Defaulted to `id`.
    # See :class:`~flask_jwt_router._config` for more information.
    entity_key: str = "id"

    #: The reference to the entity key.
    #: See :class:`~flask_jwt_router._config` for more information.
    public_key: str = None

    #: The reference to the entity key.
    #: See :class:`~flask_jwt_router._config` for more information.
    private_key: str = None

    #: The reference to the entity ID.
    entity_id: str = None

    def __init__(self):
        # pylint:disable=useless-super-delegation
        super(RSAAuthentication, self).__init__()

    def create_token(self, config: Config, exp: int, **kwargs):
        """

        """
        self.entity_id = kwargs.get("entity_id", None)
        table_name = kwargs.get("table_name", None)
        return self.encode_token(config, self.entity_id, exp, table_name)

    def encode_token(self, config: Config, entity_id: Any, exp: int, table_name: str):
        """

        """
        self.entity_key = config.entity_key
        self.secret_key = config.secret_key

        encoded = jwt.encode({
            "table_name": table_name,
            self.entity_key: entity_id,
            # pylint: disable=no-member
            "exp": datetime.utcnow() + relativedelta(days=+exp)
        }, self.private_key, algorithm="RS256")
        try:
            # Handle < pyJWT==2.0
            encoded = encoded.decode("utf-8", self.public_key, algorithms=["RS256"])
        except AttributeError:
            pass
        return encoded

    def update_token(self,
                     config: Config,
                     exp: int,
                     table_name: str,
                     **kwargs,
                     ) -> str:
        """
        kwargs:
            - entity_id: Represents the entity's primary key
        :param config:
        :param exp:
        :param table_name:
        :return: Union[str, None]
        """
        self.entity_id = kwargs.get("entity_id", None)
        return self.encode_token(config, self.entity_id, exp, table_name)

    def get_oauth_token(self) -> str:
        """
        :return: A Google OAuth 2.0 token
        """
        return g.get("access_token")

"""
     The main configuration class for Flask-JWT-Router
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Tuple

from ._entity import _ORMType


class SecretKeyError(Exception):
    message = "You must define a secret key OR public & private keys. " \
              "See https://flask-jwt-router.readthedocs.io/en/latest/extensions.html"

    def __init__(self):
        super(SecretKeyError, self).__init__(self.message)


class BaseConfig(ABC):
    """Abstract Base Class for Extensions"""

    def __init__(self):
        self.expire_days = None

    @abstractmethod
    def init_config(self, config: Dict[str, Any], **kwargs) -> None:
        # pylint: disable=missing-function-docstring
        pass


class Config(BaseConfig):
    """
    :param secret_key: User defined secret key
    :param entity_key: The entity's primary key (ie id or user_id etc.). Default is *id*
    :param whitelist_routes: List of tuple pairs of verb & url path
    :param api_name: the api name prefix e.g `/api/v1`
    :param ignored_routes: Opt our routes from api name prefixing
    :param entity_models: Multiple entities to be authenticated
    :param expire_days: Expire time for the token in days
    :param oauth_entity: If google_oauth options are declared then this will indicate the entity key in flight
    :param public_key: TODO
    :param private_key: TODO
    :kwargs:
        :param entity_models: Multiple entities to be authenticated
        :param google_oauth: Options if the type or auth is Google's OAuth 2.0
    """
    secret_key: str
    entity_key: str
    whitelist_routes: List[Tuple[str]]
    api_name: str
    ignored_routes: List[Tuple[str]]
    entity_models: List[_ORMType]
    expire_days: int
    google_oauth: Dict
    oauth_entity: str = None
    public_key: str = None
    private_key: str = None

    def init_config(self, app_config: Dict[str, Any], **kwargs) -> None:
        """
        :param app_config:
        :return:
        """
        self.secret_key = app_config.get("SECRET_KEY")
        self.entity_key = app_config.get("ENTITY_KEY") or "id"
        self.whitelist_routes = app_config.get("WHITE_LIST_ROUTES") or []
        self.api_name = app_config.get("JWT_ROUTER_API_NAME")
        self.ignored_routes = app_config.get("IGNORED_ROUTES") or []
        self.entity_models = app_config.get("ENTITY_MODELS") or kwargs.get("entity_models") or []
        self.expire_days = app_config.get("JWT_EXPIRE_DAYS")
        self.google_oauth = kwargs.get("google_oauth")
        self.public_key = app_config.get("JWT_PUBLIC_KEY")
        self.private_key = app_config.get("JWT_PRIVATE_KEY")

        if not self.secret_key and (not self.private_key or not self.public_key):
            raise SecretKeyError

        if self.google_oauth:
            self.oauth_entity = self.google_oauth["email_field"]

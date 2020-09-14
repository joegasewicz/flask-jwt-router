"""
     The main configuration class for Flask-JWT-Router
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Tuple

from ._entity import _ORMType


class SecretKeyError(Exception):
    message = "You must define a secret key. " \
              "See https://flask-jwt-router.readthedocs.io/en/latest/extensions.html"

    def __init__(self):
        super(SecretKeyError, self).__init__(self.message)


class _Config:
    def __init__(self,
                 secret_key=None,
                 entity_key="id",
                 whitelist_routes=None,
                 api_name=None,
                 ignored_routes=None,
                 entity_models=None,
                 expire_days=None,
                 ):

        self.secret_key = secret_key
        self.entity_key = entity_key
        self.whitelist_routes = whitelist_routes
        self.api_name = api_name
        self.ignored_routes = ignored_routes
        self.entity_models = entity_models
        self.expire_days = expire_days


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
    :param entity_key: The name of the model's entity attribute
    :param whitelist_routes: List of tuple pairs of verb & url path
    :param api_name: the api name prefix e.g `/api/v1`
    :param ignored_routes: Opt our routes from api name prefixing
    :param entity_models: Multiple entities to be authenticated
    :param expire_days: Expire time for the token in days
    """
    secret_key: str
    entity_key: str
    whitelist_routes: List[Tuple[str]]
    api_name: str
    ignored_routes: List[Tuple[str]]
    entity_models: List[_ORMType]
    expire_days: int

    def init_config(self, app_config: Dict[str, Any], **kwargs) -> None:
        """
        :param app_config:
        :return:
        """
        entity_models = kwargs.get("entity_models")
        _config = _Config(
            app_config.get("SECRET_KEY"),
            app_config.get("ENTITY_KEY") or "id",
            app_config.get("WHITE_LIST_ROUTES") or [],
            app_config.get("JWT_ROUTER_API_NAME"),
            app_config.get("IGNORED_ROUTES") or [],
            entity_models or app_config.get("ENTITY_MODELS") or [],
            app_config.get("JWT_EXPIRE_DAYS")
        )
        if not _config.secret_key:
            raise SecretKeyError

        self.secret_key = _config.secret_key
        self.entity_key = _config.entity_key
        self.whitelist_routes = _config.whitelist_routes
        self.api_name = _config.api_name
        self.ignored_routes = _config.ignored_routes
        self.entity_models = _config.entity_models
        self.expire_days = _config.expire_days

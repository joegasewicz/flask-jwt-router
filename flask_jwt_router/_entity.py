"""
    Entity is a service class concerned with Database / ORM / sessions & transaction
    Includes static utilities consumed by AuthStrategy classes
"""
import inspect
from abc import ABC, abstractmethod
from flask import g
from typing import Any, ClassVar, List, Tuple, Dict, Union, Optional

_ORMType = type(List[Tuple[int, str]])


class NoTokenInHeadersError(Exception):
    message = "No token in headers error!\n" \
              "Did you mean to call create_token? " \
              "See https://flask-jwt-router.readthedocs.io/en/latest/jwt_routes.html#authorization-tokens"

    def __init__(self, err):
        super(NoTokenInHeadersError, self).__init__(f"{err}\n{self.message}")


class BaseEntity(ABC):
    # pylint:disable=missing-class-docstring

    @property
    @abstractmethod
    def entity_key(self) -> str:
        # pylint:disable=missing-function-docstring
        pass

    @abstractmethod
    def get_attr_name(self, table_name: str = None) -> str:
        # pylint:disable=missing-function-docstring
        pass

    @abstractmethod
    def get_entity_from_token_or_tablename(self, decoded_token: str = None, *, tablename=None, email_value=None) -> str:
        # pylint:disable=missing-function-docstring
        pass

    @abstractmethod
    def get_entity_from_ext(self, table_name: str = None) -> _ORMType:
        # pylint:disable=missing-function-docstring
        pass

    @abstractmethod
    def clean_up(self) -> None:
        # pylint:disable=missing-function-docstring
        pass



class Entity(BaseEntity):
    """
    :param config:
    :param auth_model:
    """

    #: The result from the decoded token.
    #: This gets assigned in :class:`~get_entity_from_token`
    decoded_token: Dict[str, Any] = None

    #: The assigned entity model in the current request
    #: This gets assigned in :class:`~flask_jwt_router._entity.get_entity_from_token`
    auth_model: _ORMType = None

    #: The table name value from :class: `~flask_jwt_router.oauth2.google`. This
    #: indicates we are now using oauth 2.0.
    tablename: Optional[str] = None

    #: This will override the config.entity_key for oauth 2.0 in flight tokens
    _oauth_entity_key: str = None

    entity_key: str = None

    def __init__(self, config: ClassVar):
        self.config = config

    @property
    def oauth_entity_key(self):
        return self._oauth_entity_key

    @oauth_entity_key.setter
    def oauth_entity_key(self, val: str):
        self._oauth_entity_key = val

    def get_attr_name(self, table_name: str = None) -> str:
        """
        If SQLAlchemy is the ORM then expect there to be a
        __mapper__.primary_key path. This returns a list
        but for our purposes we only need the first
        primary key attribute name. This method maintains the
        existing option of specifying a primary key name directly
        for scenarios when not using SqlAlchemy etc.
        :param table_name:
        :return:
        """
        if not self.auth_model:
            self.auth_model = self.get_entity_from_ext(table_name)
        if hasattr(self.auth_model, "__mapper__"):
            # SqlAlchemy is the ORM being used
            return self.auth_model.__mapper__.primary_key[0].name
        return self.entity_key

    def _get_from_model(self, entity_key: str, entity_value: Any) -> _ORMType:
        """
        :param entity_key: The SqlAlchemy field name to query against
        :param entity_value: The field row value to filter with
        :return: {_ORMType}
        """
        # entity_key: str = self.get_attr_name()
        result = self.auth_model.query.filter_by(**{entity_key: entity_value}).one()
        return result

    def get_entity_from_ext(self, tablename: str = None) -> _ORMType:
        """
        Exception raised if SQLAlchemy ORM not being used
        (SQLAlchemy will throw if `__tablename__` doesn't exist
        or it can't create the name from the db engine's table object.
        :return: {_ORMType}
        """
        # If oauth 2.0 is active then self.tablename has priority
        self.tablename = self.tablename or tablename
        if not self.tablename:
            # In case `update_token()` is called, `table_name` is in the token
            try:
                self.tablename = self.decoded_token.get("table_name")
            except AttributeError as err:
                raise NoTokenInHeadersError(err)
        auth_model = None

        for model in self.config.entity_models:
            if hasattr(model, "__tablename__"):
                if self.tablename == model.__tablename__:
                    auth_model = model
            else:
                raise Exception(
                    "[FLASK-JWT-ROUTER ERROR]: Your Entity model must have a `__tablename__` that"
                    " is equal to the table_name specified in create_token()."
                    "For details visit:\n"
                    # pylint:disable=line-too-long
                    "https://flask-jwt-router.readthedocs.io/en/latest/jwt_routes.html#authorization-tokens"
                )
        if auth_model:
            return auth_model
        raise Exception(
            "[FLASK-JWT-ROUTER ERROR]: Your Entity model must have a `__tablename__` attribute!"
            " If you are running flask-jwt-router against tests, make sure"
            " you assign a `__tablename__` attribute to your Model class."
        )

    def get_entity_from_token_or_tablename(
            self,
            decoded_token: Dict[str, any] = None,
            *,
            tablename=None,
            email_value=None,
    ) -> Union[str, None]:
        """
        Entity class main public method.
        Attaches a __get_entity__ method to the AuthModel class &
        calling the attached method returns the entity data
        :param decoded_token: {Dict[str, Any]}
        :kwargs:
            :param tablename: This is passed in directly from any oauth 2.0 sessions
        :return: {str}
        """
        if decoded_token:
            self.decoded_token = decoded_token
        if tablename:
            # This means that the user has logged in via a oauth 2.0 strategy
            self.tablename = tablename
        self.auth_model = self.get_entity_from_ext()
        entity_key: str = self.get_attr_name()
        self._attach_method()
        try:
            # If self.oauth_entity_key exists then we have a google oauth 2.0 access token
            if self.oauth_entity_key:
                result = self.auth_model.__get_entity__(self.oauth_entity_key, email_value)
            else:
                result = self.auth_model.__get_entity__(entity_key, decoded_token[self.get_attr_name()])
            return result
        except KeyError as _:
            return None

    def _attach_method(self) -> None:
        """
        Check if __get__entity__ doesn't already exist & attach
        __get_entity__ onto the entity model class
        :return: None
        """
        methods = inspect.getmembers(self.auth_model, predicate=inspect.ismethod)
        for method in methods:
            if method == "__get_entity__":
                raise ValueError("__get_entity__ method already exists")
        setattr(
            self.auth_model,
            "__get_entity__",
            self._get_from_model
        )

    def clean_up(self) -> None:
        """
        Cleans up the following from the previous request:
            - oauth_entity_key
            - tablename
            - Removes any entities from g contained in config.entity_models
        """
        self.oauth_entity_key = None
        self.tablename = None
        # This removes all entities attached from the previous request
        for v in self.config.entity_models:
            if hasattr(g, v.__tablename__):
                delattr(g, v.__tablename__)

"""
    Entity is a service class concerned with Database / ORM / sessions & transaction
    Includes static utilities consumed by AuthStrategy classes
"""
import inspect
from abc import ABC, abstractmethod
from typing import Any, ClassVar, List, Tuple, Dict, Union

_ORMType = type(List[Tuple[int, str]])


class BaseEntity(ABC):

    @abstractmethod
    def get_attr_name(self) -> str:
        pass

    @abstractmethod
    def get_entity_from_token(self, decoded_token: str) -> str:
        pass

    @abstractmethod
    def get_entity_from_ext(self) -> _ORMType:
        pass


class Entity(BaseEntity):
    """
    :param extensions:
    :param auth_model:
    """

    #: The result from the decoded token.
    #: This gets assigned in :class:`~get_entity_from_token`
    decoded_token: Dict[str, Any] = None

    #: The assigned entity model in the current request
    #: This gets assigned in :class:`~flask_jwt_router._entity.get_entity_from_token`
    auth_model: _ORMType = None

    def __init__(self, extensions: ClassVar):
        self.extensions = extensions

    def get_attr_name(self, entity_type: str = None) -> str:
        """
        :description: If SQLAlchemy is the ORM then expect there to be a
        __mapper__.primary_key path. This returns a list
        but for our purposes we only need the first
        primary key attribute name. This method maintains the
        existing option of specifying a primary key name directly
        for scenarios when not using SqlAlchemy etc & also assigns
        a default primary key to `id`.
        :return: {str}
        """
        if not self.auth_model:
            self.auth_model = self.get_entity_from_ext(entity_type)
        if hasattr(self.auth_model, "__mapper__"):
            """SqlAlchemy is the ORM being used"""
            return self.auth_model.__mapper__.primary_key[0].name
        else:
            return self.extensions.entity_key

    def _get_from_model(self, entity_id: int) -> _ORMType:
        """
        :param entity_id:
        :return: {_ORMType}
        """
        entity_key: str = self.get_attr_name()
        result = self.auth_model.query.filter_by(**{entity_key: entity_id}).one()
        return result

    def get_entity_from_ext(self, entity_type: str = None) -> _ORMType:
        """
        Exception raised if SQLAlchemy ORM not being used
        (SQLAlchemy will throw if `__tablename__` doesn't exist
        or it can't create the name from the db engine's table object.
        :return: {_ORMType}
        """
        if not entity_type:
            # In case `update_entity()` is called, `entity_type` is in the token
            entity_type = self.decoded_token.get("entity_type")
        auth_model = None

        for model in self.extensions.entity_models:
            if hasattr(model, "__tablename__"):
                if entity_type == model.__tablename__:
                    auth_model = model
            else:
                raise Exception(
                    "[FLASK-JWT-ROUTER ERROR]: Your Entity model must have a `__tablename__` that"
                    " is equal to the entity_type specified in register_entity(). For details visit:\n"
                    " https://flask-jwt-router.readthedocs.io/en/latest/jwt_routes.html#authorization-tokens"
                )
        if auth_model:
            return auth_model
        else:
            raise Exception(
                "[FLASK-JWT-ROUTER ERROR]: Your Entity model must have a `__tablename__` attribute!"
                " If you are running flask-jwt-router against tests, make sure"
                " you assign a `__tablename__` attribute to your Model class."
            )

    def get_entity_from_token(self, decoded_token: Dict[str, any]) -> Union[str, None]:
        """
        Entity class main public method.
        Attaches a __get_entity__ method to the AuthModel class &
        calling the attached method returns the entity data
        :param decoded_token: {Dict[str, Any]}
        :return: {str}
        """
        self.decoded_token = decoded_token
        self.auth_model = self.get_entity_from_ext()
        self._attach_method()
        try:
            result = self.auth_model.__get_entity__(decoded_token[self.get_attr_name()])
            return result
        except KeyError as err:
            # TODO log err for dev here
            return None

    def _attach_method(self) -> None:
        """
        Check if __get__entity__ doesn't already exists & attach
        __get_entity__ onto the entity model class
        :return: None
        """
        methods = inspect.getmembers(self.auth_model, predicate=inspect.ismethod)
        for m in methods:
            if m == "__get_entity__":
                raise ValueError("__get_entity__ method already exists")
        setattr(
            self.auth_model,
            "__get_entity__",
            self._get_from_model
        )

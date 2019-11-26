"""
    Entity is a service class concerned with Database / ORM / sessions & transaction
    Includes static utilities consumed by AuthStrategy classes
"""
import inspect
from abc import ABC, abstractmethod
from typing import Any, ClassVar, List, Tuple, Dict

_ORMType = type(List[Tuple[int, str]])


class BaseEntity(ABC):

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

    def get_entity_model(self):
        pass

    def _get_from_model(self, entity_id: int) -> _ORMType:
        """
        :param entity_id:
        :return: {_ORMType}
        """
        entity_key: str = self.extensions.entity_key
        result = self.auth_model.query.filter_by(**{entity_key: entity_id}).one()
        return result

    def get_entity_from_ext(self) -> _ORMType:
        """
        Exception raised if SQLAlchemy ORM not being used
        (SQLAlchemy will throw if `__tablename__` doesn't exist
        or it can't create the name from the db engine's table object.
        :return: {_ORMType}
        """
        entity_type = self.decoded_token.get("entity_type")
        auth_model = None
        for model in self.extensions.entity_models:
            if hasattr(model, "__tablename__") and entity_type == model.__tablename__:
                auth_model = model
        if auth_model:
            return auth_model
        else:
            raise Exception(
                "[FLASK-JWT-ROUTER ERROR]: Your Entity model must have a `__tablename__` attribute!"
                " If you are running flask-jwt-router against tests, make sure"
                " you assign a `__tablename__` attribute to your Model class."
            )

    def get_entity_from_token(self, decoded_token: Dict[str, any]) -> str:
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
        result = self.auth_model.__get_entity__(decoded_token[self.extensions.entity_key])
        return result

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

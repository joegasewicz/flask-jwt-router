"""
    Entity is a service class concerned with Database / ORM / sessions & transaction
    Includes static utilities consumed by AuthStrategy classes
"""
import inspect
from abc import ABC, abstractmethod
from typing import Union, Any, ClassVar


class BaseEntity(ABC):

    @staticmethod
    @abstractmethod
    def get_entity_id(self, **kwargs) -> Union[str, None]:
        pass

    @staticmethod
    @abstractmethod
    def set_entity_model(model) -> Any:
        pass

    @abstractmethod
    def get_id_from_token(self, decoded_token: str) -> str:
        pass


class Entity(BaseEntity):
    """

    :param extensions:
    :param auth_model:
    """
    def __init__(self, extensions: ClassVar, auth_model: Any):
        self.extensions = extensions
        self.auth_model = auth_model

    @staticmethod
    def get_entity_id(**kwargs) -> Union[str, None]:
        """
        :param kwargs: Dict[str, int]
        :return: Union[str, None]
        """
        try:
            return kwargs['entity_id']
        except KeyError as _:
            return None

    def _get_user_from_auth_model(self, entity_id: int) -> Any:
        """
        :param entity_id:
        :return: Any
        """
        entity_key: str = self.extensions.entity_key
        result = self.auth_model.query.filter_by(**{entity_key: entity_id}).one()
        return result

    def get_id_from_token(self, decoded_token: str) -> str:
        """
        Attaches a __get_entity__ method to the AuthModel class &
        calling the attached method returns the entity data
        :param decoded_token:
        :return:
        """
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
            self._get_user_from_auth_model
        )

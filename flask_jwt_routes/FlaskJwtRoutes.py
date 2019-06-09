from abc import ABC, abstractmethod

import logging
logger = logging.getLogger()


class FlaskJwtRoutesABC(ABC):

    @abstractmethod
    def get_app_config(self, app):
        pass

    @abstractmethod
    def get_entity_key(self):
        pass

    @abstractmethod
    def get_entity_id(self, kwargs):
        pass

    @abstractmethod
    def get_exp(self, kwargs):
        pass

    @abstractmethod
    def get_secret_key(self):
        pass

    @staticmethod
    def set_entity_model(kwargs):
        pass


class FlaskJwtRoutes(FlaskJwtRoutesABC):

    logger = logger
    """Flask JWT Router logger"""
    config = {}
    """Flask Configuration object"""
    app = None
    """Flask app instance"""
    exp = 30
    """Default exp"""
    secret_key = "DEFAULT_SECRET_KEY"
    """Default secret key"""
    entity_key = "id"
    """Primary key for the entity id"""
    _auth_model = None
    """ An SQLAlchemy Model entity instance"""

    def __init__(self, app=None, **kwargs):
        self.app = app
        config = self.get_app_config(app)
        self.config = config

    def get_app_config(self, app):
        """
        :param app: Flask Application Instance
        :return: Dict[str, Any]
        """
        return getattr(app, "config", {})

    def get_entity_key(self):
        """
        :return: str
        """
        if "ENTITY_KEY" in self.config and self.config["ENTITY_KEY"] is not None:
            return self.config["ENTITY_KEY"]
        else:
            return self.entity_key

    def get_entity_id(self, kwargs):
        """
        :param kwargs: Dict[str, int]
        :return: str
        """
        try:
            return kwargs['entity_id']
        except KeyError as _:
            return None

    def get_exp(self, kwargs):
        """
        :param kwargs: Dict[str, int]
        :return: number
        """
        try:
            return kwargs['exp']
        except KeyError as _:
            return 30

    def get_secret_key(self):
        """
        :return: str
        """
        if "SECRET_KEY" in self.config and self.config["SECRET_KEY"] is not None:
            return self.config["SECRET_KEY"]
        else:
            self.logger.warning("Warning: Danger! You have't set a SECRET_KEY in your flask app.config")
            return self.secret_key

    @property
    def auth_model(self):
        return self._auth_model

    @auth_model.setter
    def auth_model(self, value):
        self._auth_model = value

    @staticmethod
    def set_entity_model(kwargs):
        if "entity_model" in kwargs and kwargs["entity_model"] is not None:
            return kwargs["entity_model"]


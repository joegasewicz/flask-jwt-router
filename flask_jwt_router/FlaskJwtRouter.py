from abc import ABC, abstractmethod

import logging
logger = logging.getLogger()


class FlaskJwtRouterABC(ABC):

    @abstractmethod
    def init_app(selfself, app):
        pass

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


class FlaskJwtRouter(FlaskJwtRouterABC):

    logger = logging
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
        """
        - If there app is None then self.init_app(app=None, **kwargs) need to be called
            inside the Flask app factory pattern
        :param app:
        :param kwargs:
        """
        if app:
            self.app = app
            config = self.get_app_config(app)
            self.config = config

    def init_app(self, app, **kwargs):
        self.app = app
        config = self.get_app_config(app)
        self.config = config

    def get_app_config(self, app):
        """
        :param app: Flask Application Instance
        :return: Dict[str, Any]
        """
        config = getattr(app, "config", {})
        return config

    def get_entity_key(self):
        """
        :return: str
        """
        if "ENTITY_KEY" in self.config and self.config["ENTITY_KEY"] is not None:
            return self.config["ENTITY_KEY"]
        else:
            return self.entity_key

    def get_entity_id(self, **kwargs):
        """
        :param kwargs: Dict[str, int]
        :return: str
        """
        try:
            return kwargs['entity_id']
        except KeyError as _:
            return None

    def get_exp(self, **kwargs):
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
    def set_entity_model(model):
        if "entity_model" in model and model["entity_model"] is not None:
            return model["entity_model"]



import logging

from flask_jwt_router._extensions import BaseExtension, Extensions, Config
from flask_jwt_router._entity import BaseEntity, Entity
from flask_jwt_router._routing import BaseRouting, Routing

logger = logging.getLogger()


class FlaskJWTRouter:

    logger = logging
    config = {}
    app = None
    exp = 30
    _auth_model = None
    extensions: Config

    def __init__(self, app=None, **kwargs):
        """
        If there app is None then self.init_app(app=None, **kwargs) need to be called
        inside the Flask app factory pattern
        :param app:
        :param kwargs:
        """
        self.entity: BaseEntity = Entity(self.extensions, Entity.set_entity_model(kwargs))
        self.ext: BaseExtension = Extensions()
        self.routing: BaseRouting = Routing()

        if app:
            self.init_app(app)

    def init_app(self, app):
        """
        You can use this to set up your config at runtime
        :param app:
        :param kwargs:
        :return:
        """
        self.app = app
        config = self.get_app_config(app)
        self.config = config
        self.extensions = self.ext.init_extensions(config)
        self.app.before_request(self.routing.before_middleware)

    def get_app_config(self, app):
        """
        :param app: Flask Application Instance
        :return: Dict[str, Any]
        """
        config = getattr(app, "config", {})
        return config

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
            return self.extensions.secret_key

    @property
    def auth_model(self):
        return self._auth_model

    @auth_model.setter
    def auth_model(self, value):
        self._auth_model = value




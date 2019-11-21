import logging
from typing import ClassVar

from ._extensions import BaseExtension, Extensions, Config
from ._entity import BaseEntity, Entity
from ._routing import BaseRouting, Routing
from ._authentication import BaseAuthStrategy

logger = logging.getLogger()


class FlaskJWTRouter:
    """
    If there app is None then self.init_app(app=None, **kwargs) need to be called
    inside the Flask app factory pattern
    :param app:
    :param kwargs:
    """
    logger = logging
    app = None
    exp = 30
    _auth_model: ClassVar = None
    extensions: Config
    auth: BaseAuthStrategy
    entity: BaseEntity
    routing: BaseRouting
    ext: BaseExtension

    def __init__(self, app=None, **kwargs):
        self.ext = Extensions()
        _auth_model = kwargs.get("entity_model", None)

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
        self.extensions = self.ext.init_extensions(config)
        self.entity = Entity(self.extensions, self.auth_model)
        self.routing = Routing(self.app, self.extensions, self.entity)
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

    @property
    def auth_model(self):
        return self._auth_model

    @auth_model.setter
    def auth_model(self, value):
        """
        :param value:
        :return:
        """
        self._auth_model = value

    def register_entity(self, **kwargs) -> str:
        """
        :param kwargs:
        :return:
        """
        return self.auth.register_entity(self.extensions, self.exp, **kwargs)

    def update_entity(self, **kwargs) -> str:
        """
        :param kwargs:
        :return:
        """
        return self.auth.update_entity(self.extensions, self.exp, **kwargs)

    def encode_token(self, entity_id) -> str:
        """
        :param entity_id:
        :return:
        """
        return self.auth.encode_token(self.extensions, entity_id, self.exp)

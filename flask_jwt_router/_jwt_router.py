import logging

from ._extensions import BaseExtension, Extensions, Config
from ._entity import BaseEntity, Entity
from ._routing import BaseRouting, Routing
from ._authentication import BaseAuthStrategy

logger = logging.getLogger()


class FlaskJWTRouter:
    """
    If there app is None then self.init_app(app=None, **kwargs) need to be called
    inside the Flask app factory pattern

    :param app: Flask application instance
    :param kwargs: entity_model
    """

    #: Logging.
    logger = logging

    #: The Flask application instance.
    app = None

    #: Token expiry value. eg. 30 = 30 days from creation date.
    exp: int = 30

    #: The class that is used to create Config objects.  See :class:`~flask_jwt_router._extensions`
    #: for more information.
    extensions: Config

    #: The class that provides algorithms to :class:`~flask_jwt_router._jwt_routes`.
    # See :class:`~flask_jwt_router._authentication` for more information.
    auth: BaseAuthStrategy

    #: The class that is used to create Entity objects.  See :class:`~flask_jwt_router._entity`
    #: for more information.
    entity: BaseEntity

    #: The class that is used to create Routing objects.  See :class:`~flask_jwt_router._routing`
    #: for more information.
    routing: BaseRouting

    #: The class that is used to create Config objects.  See :class:`~flask_jwt_router._extensions`
    #: for more information.
    ext: BaseExtension

    def __init__(self, app=None, **kwargs):
        self.ext = Extensions()
        if app:
            self.init_app(app)

    def init_app(self, app):
        """
        You can use this to set up your config at runtime
        :param app: Flask application instance
        :return:
        """
        self.app = app
        config = self.get_app_config(app)
        self.extensions = self.ext.init_extensions(config)
        self.entity = Entity(self.extensions)
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
        entity_type = self.entity.get_entity_from_ext().__tablename__
        return self.auth.update_entity(self.extensions, self.exp, entity_type, **kwargs)

    def encode_token(self, entity_id) -> str:
        """
        :param entity_id:
        :return:
        """
        entity_type = self.entity.get_entity_from_ext().__tablename__
        return self.auth.encode_token(self.extensions, entity_id, self.exp, entity_type)

import logging
logger = logging.getLogger()

from flask_jwt_router._extensions import _Extensions


class FlaskJWTRouter:

    logger = logging
    config = {}
    app = None
    exp = 30
    _auth_model = None
    extensions: _Extensions

    def __init__(self, app=None, **kwargs):
        """
        If there app is None then self.init_app(app=None, **kwargs) need to be called
        inside the Flask app factory pattern
        :param app:
        :param kwargs:
        """
        self.auth_model = FlaskJwtRouter.set_entity_model(kwargs)
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
        self.extensions = self.init_extensions(config)
        self.app.before_request(self._before_middleware)

    def init_flask_jwt_router(self, config):
        config = _Extensions(
            config.get("SECRET_KEY") or "DEFAULT_SECRET_KEY",
            config.get("ENTITY_KEY"),
            config.get("WHITE_LIST_ROUTES") or [],
            config.get("JWT_ROUTER_API_NAME"),
            config.get("IGNORED_ROUTES") or [],
        )
        return config

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

    @staticmethod
    def set_entity_model(model):
        if "entity_model" in model and model["entity_model"] is not None:
            return model["entity_model"]



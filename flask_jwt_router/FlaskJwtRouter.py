import logging
logger = logging.getLogger()


class _Config:
    """
    :param secret_key: Defaults to `DEFAULT_SECRET_KEY`
    :param entity_key: The name of the model's entity attribute
    :param whitelist_routes: List of tuple pairs of verb & url path
    :param api_name: the api name prefix e.g `/api/v1`
    :param ignored_routes: Opt our routes from api name prefixing
    """
    def __init__(self,
                 secret_key=None,
                 entity_key="id",
                 whitelist_routes=None,
                 api_name=None,
                 ignored_routes=None
                 ):

        self.secret_key = secret_key
        self.entity_key = entity_key
        self.whitelist_routes = whitelist_routes
        self.api_name = api_name
        self.ignored_routes = ignored_routes


class FlaskJwtRouter:

    logger = logging
    config = {}
    app = None
    exp = 30
    _auth_model = None
    extensions: _Config

    def __init__(self, app=None, **kwargs):
        """
        If there app is None then self.init_app(app=None, **kwargs) need to be called
        inside the Flask app factory pattern
        :param app:
        :param kwargs:
        """
        pass

    def init_flask_jwt_router(self, config):
        config = _Config(
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

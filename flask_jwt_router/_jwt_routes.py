"""
    Quick Start
    ===========

    Installation::

       pip install flask-jwt-router


    Basic Usage::

        from flask import Flask
        from flask_jwt_router import JwtRoutes

        app = Flask(__name__)

        JwtRoutes(app)

        # If you're using the Flask factory pattern:
        jwt_routes = JwtRoutes()

        def create_app(config):
            ...
            jwt_routes.init_app(app)


    Authorizing Routes
    ==================

    Define as a list of tuples::

        app.config["WHITE_LIST_ROUTES"] = [
            ("POST", "/register"),
        ]

        @app.route("/register", methods=["POST"])
        def register():
            return "I don't need authorizing!"


    Prefix your api name to whitelisted routes::

        # All routes will
        app.config["JWT_ROUTER_API_NAME"] = "/api/v1"
        app.config["WHITE_LIST_ROUTES"] = [
            ("POST", "/register"),
        ]

        @app.route("/api/v1/register", methods=["POST"])
        def register():
            return "I don't need authorizing!"


    Bypass Flask-JWT-Router on specified routes::

        # Define homepage template routes for example on JWT_IGNORE_ROUTES
        # & still get to use the api name on request handlers returning resources

        app.config["IGNORED_ROUTES"] = [
            ("GET", "/")
        ]


    Declare an entity model::

        # Create your entity model (example uses Flask-SqlAlchemy)

        class UserModel(db.Model):
            __tablename__ = "users"
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String)

        JwtRoutes(app, entity_models=[UserModel, TeacherModel, ...etc])

        # Or pass later with `init_app`
        def create_app(config):
            ...
            jwt_routes.init_app(app, entity_models=[UserModel, TeacherModel, ...etc])


    Authorization & Tokens
    ======================

    From your_app import jwt_routes::

        # white list the routes
        app.config["WHITE_LIST_ROUTES"] = [
            ("POST", "/register"),
            ("POST", "/login"),
        ]

        @app.route("/register", methods=["POST"])
        def register():
            # I'm registering a new user & returning a token!
            return jsonify({
                "token": jwt_routes.create_token(entity_id=1)
            })

        @app.route("/login", methods=["POST"])
        def login():
            # I'm authorized & updating my token!
            return jsonify({
                "token": jwt_routes.update_token(entity_id=1)
            })

    Create a new entity & return a new token::

        @app.route("/register", methods=["POST"])
        def register():
            user_data = request.get_json()
            try:
                user = UserModel(**user_data)
                user.create_user() # your entity creation logic

                # Here we pass the id as a kwarg to `create_token`
                token: str = jwt_routes.create_token(entity_id=user.id, table_name="user")

                # Now we can return a new token!
                return {
                    "message": "User successfully created.",
                    "token": str(token),  # casting is optional
                }, 200

    Access entity on Flask's global context::

        from app import app, jwt_routes

        # Example uses Marshmallow to serialize entity object

        @app.route("/login" methods=["GET"])
        def login():
            user_data = g.get("entity")
            try:
                user_dumped = UserSchema().dump(user_data)
            except ValidationError as _:
               return {
                           "error": "User requested does not exist."
                       }, 401
            return {
                "data": user_dumped,
                "token": jwt_routes.create_token(entity_id=user_data.id, table_name="user"),
            }, 200

    If you are handling a request with a token in the headers you can call::

        jwt_routes.update_token(entity_id=user_data.id)

    If you are handling a request without a token in the headers you can call::

        jwt_routes.create_token(entity_id=user_data.id, table_name="user")

"""

import logging
from warnings import warn
from typing import List

from ._config import BaseConfig, Config, _Config
from ._entity import BaseEntity, Entity, _ORMType
from ._routing import BaseRouting, Routing
from ._authentication import BaseAuthentication, Authentication

# pylint:disable=invalid-name
logger = logging.getLogger()


class JwtRoutes:
    """
        If there app is None then self.init_app(app=None, **kwargs) need to be called
        inside the Flask app factory pattern.
    :param app: Flask application instance
    :param kwargs: entity_model
    """
    #: Logging.
    logger = logging

    #: The Flask application instance.
    app = None

    #: A list of entity models
    entity_models: List[_ORMType]

    #: Token expiry value. eg. 30 = 30 days from creation date.
    exp: int = 30

    #: The class that is used to create Config objects.  See :class:`~flask_jwt_router._config`
    #: for more information.
    config: _Config

    #: The class that provides algorithms to :class:`~flask_jwt_router._jwt_routes`.
    # See :class:`~flask_jwt_router._authentication` for more information.
    auth: BaseAuthentication

    #: The class that is used to create Entity objects.  See :class:`~flask_jwt_router._entity`
    #: for more information.
    entity: BaseEntity

    #: The class that is used to create Routing objects.  See :class:`~flask_jwt_router._routing`
    #: for more information.
    routing: BaseRouting

    #: The class that is used to create Config objects.  See :class:`~flask_jwt_router._config`
    #: for more information.
    ext: BaseConfig

    def __init__(self, app=None, **kwargs):
        self.entity_models = kwargs.get("entity_models")
        self.ext = Config()
        self.auth = Authentication()
        self.app = app
        if app:
            self.init_app(app, entity_models=self.entity_models)

    def init_app(self, app=None, **kwargs):
        """
        You can use this to set up your config at runtime
        :param app: Flask application instance
        :return:
        """
        self.app = app if app else self.app
        entity_models = self.entity_models or kwargs.get("entity_models")
        config = self.get_app_config(self.app)
        self.config = self.ext.init_config(config, entity_models=entity_models)
        self.entity = Entity(self.config)
        self.routing = Routing(self.app, self.config, self.entity)
        self.app.before_request(self.routing.before_middleware)

    # pylint:disable=no-self-use
    def get_app_config(self, app):
        """
        :param app: Flask Application Instance
        :return: Dict[str, Any]
        """
        config = getattr(app, "config", {})
        return config

    # pylint:disable=no-self-use
    def get_entity_id(self, **kwargs):
        """
        :param kwargs: Dict[str, int]
        :return: str
        """
        try:
            return kwargs['entity_id']
        except KeyError as _:
            return None
    # pylint:disable=no-self-use

    def get_exp(self, **kwargs):
        """
        :param kwargs: Dict[str, int]
        :return: number
        """
        try:
            return kwargs['exp']
        except KeyError as _:
            return 30

    def create_token(self, **kwargs) -> str:
        """
        :param kwargs:
        :return: str
        """
        if 'entity_type' in kwargs:
            warn(("'entity_type' argument name has been deprecated and will be replaced"
                  "in the next release. Use 'table_name' instead"))
            kwargs['table_name'] = kwargs['entity_type']
        if 'table_name' not in kwargs:
            raise KeyError("create_token() missing 1 required argument: table_name")
        table_name = kwargs.get("table_name")
        self.config.entity_key = self.entity.get_attr_name(table_name)
        return self.auth.create_token(self.config, self.exp, **kwargs)

    def update_token(self, **kwargs) -> str:
        """
        :param kwargs:
        :return: str
        """
        self.config.entity_key = self.entity.get_attr_name()
        table_name = self.entity.get_entity_from_ext().__tablename__
        return self.auth.update_token(self.config, self.exp, table_name, **kwargs)

    def encode_token(self, entity_id) -> str:
        """
        :param entity_id:
        :return:
        """
        self.config.entity_key = self.entity.get_attr_name()
        table_name = self.entity.get_entity_from_ext().__tablename__
        return self.auth.encode_token(self.config, entity_id, self.exp, table_name)

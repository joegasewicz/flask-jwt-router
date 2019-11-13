from flask import request, abort, g
import jwt
import inspect

from .FlaskJwtRouter import FlaskJwtRouter


class JwtRoutes(FlaskJwtRouter):

    def __init__(self, app=None, **kwargs):
        super().__init__(app, **kwargs)

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
        self.extensions = self.init_flask_jwt_router(config)
        self.app.before_request(self._before_middleware)

    def _prefix_api_name(self, w_routes=[]):
        """
        If the config has JWT_ROUTER_API_NAME defined then
        update each white listed route with an api name
        :example: "/user" -> "/api/v1/user"
        :param w_routes:
        :return List[str]:
        """
        api_name = self.extensions.api_name
        if not api_name:
            return w_routes
        # Prepend the api name to the white listed route
        named_white_routes = []
        for route_name in w_routes:
            verb, path = route_name
            named_white_routes.append((verb, f"{api_name}{path}"))
        return named_white_routes

    def _add_static_routes(self, path: str):
        """
        Always allow /static/ in path and handle static_url_path from Flask **kwargs
        :param path:
        :return:
        """
        if path == "favicon.ico":
            return True

        paths = path.split("/")
        if paths[1] == "static":
            return True

        defined_static = self.app.static_url_path[1:]
        if paths[1] == defined_static:
            return True

    def _handle_query_params(self, white_route: str, path: str):
        """
        Handles dynamic query params
        All we care about that a path segment has no url conversion.
        We compare it's the same as the whitelist segment & let Flask
        / Werkzeug handle the url matching
        :param white_route:
        :param path:
        :return bool:
        """
        if "<" not in white_route:
            return False

        route_segments = white_route.split("/")
        path_segments = path.split("/")

        for r, p in zip(route_segments, path_segments):
            if len(r):
                if r[0] != "<":
                    if r != p:
                        return False
        return True

    def _allow_public_routes(self, white_routes):
        """
        Create a list of tuples ie [("POST", "/users")] as public routes.
        Returns False if current route and verb are white listed.
        :param flask_request:
        :param white_routes: List[Tuple]:
        :returns bool:
        """
        method = request.method
        path = request.path

        for white_route in white_routes:
            if method == white_route[0] and path == white_route[1]:
                return False
            if method == white_route[0] and self._handle_query_params(white_route[1], path):
                return False
        return True

    def _before_middleware(self):
        """
        Handles ignored & whitelisted & static routes with api name
        If it's not static, ignored whitelisted then authorize
        :return: Callable or None
        """
        print('here-------> ')
        path = request.path
        is_static = self._add_static_routes(path)
        if not is_static:
            # Handle ignored routes
            is_ignored = False
            ignored_routes = self.extensions.ignored_routes
            print('here-------> ', ignored_routes)
            if len(ignored_routes):
                print('here-------> ')
                is_ignored = not self._allow_public_routes(ignored_routes)
            if not is_ignored:
                white_routes = self._prefix_api_name(self.extensions.whitelist_routes)
                not_whitelist = self._allow_public_routes(white_routes)

                if not_whitelist:
                    self._handle_token()

    def _handle_token(self):
        """
        TODO exception from jwt
        Checks the headers contain a Bearer string OR params.
        Checks to see that the route is white listed.
        :return None:
        """
        try:
            if request.args.get("auth"):
                token = request.args.get("auth")
            else:
                bearer = request.headers.get("Authorization")
                token = bearer.split("Bearer ")[1]
        except Exception as err:
            self.logger.error(err)
            return abort(401)

        try:
            decoded_token = jwt.decode(
                token,
                self.extensions.secret_key,
                algorithms="HS256"
            )
        except Exception as err:
            self.logger.error(err)
            return abort(401)

        if self.auth_model is not None:
            try:
                g.entity = self._update_model_entity(decoded_token)
            except Exception as err:
                self.logger.error(err)
                return abort(401)

    def _get_user_from_auth_model(self, entity_id):
        """
        :param entity_id:
        :return: Any - TODO correct return type
        """
        entity_key: str = self.extensions.entity_key
        result = self.auth_model.query.filter_by(**{entity_key: entity_id}).one()
        return result

    def _update_model_entity(self, token):
        """
        :param token:
        :return: user Dict[str, Any] or None - TODO correct type
        """
        self._set_auth_model()
        result = self.auth_model.__get_entity__(token[self.extensions.entity_key])
        return result

    def _set_auth_model(self):
        """
        Check if __get__entity__ doesn't already exists & attach
        the method onto the entity model
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

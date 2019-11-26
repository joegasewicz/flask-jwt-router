from flask import request, abort, g
import jwt
from jwt.exceptions import InvalidTokenError
from abc import ABC, abstractmethod
import logging

from ._entity import BaseEntity

logger = logging.getLogger()


class BaseRouting(ABC):

    @abstractmethod
    def before_middleware(self) -> None:
        pass


class Routing(BaseRouting):

    def __init__(self, app, extensions, entity: BaseEntity):
        self.app = app
        self.extensions = extensions
        self.logger = logger
        self.entity = entity

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

    def _handle_pre_flight(self, method: str, w_method: str) -> bool:
        """
        Handle pre-flight requests with any verb
        TODO Investigate if this requires returning True on all valid VERBS...?\
         + tests required for this when investigated
        :param method:
        :param w_method:
        :return: {bool}
        """
        if method == w_method:
            return True
        elif method == "OPTIONS" and w_method == "POST":
            return True
        else:
            return False

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
            if self._handle_pre_flight(method, white_route[0]) and path == white_route[1]:
                return False
            if method == white_route[0] and self._handle_query_params(white_route[1], path):
                return False
        return True

    def before_middleware(self) -> None:
        """
        Handles ignored & whitelisted & static routes with api name
        If it's not static, ignored whitelisted then authorize
        :return: Callable or None
        """
        path = request.path
        is_static = self._add_static_routes(path)
        if not is_static:
            # Handle ignored routes
            is_ignored = False
            ignored_routes = self.extensions.ignored_routes
            if len(ignored_routes):
                is_ignored = not self._allow_public_routes(ignored_routes)
            if not is_ignored:
                white_routes = self._prefix_api_name(self.extensions.whitelist_routes)
                not_whitelist = self._allow_public_routes(white_routes)

                if not_whitelist:
                    self._handle_token()

    def _handle_token(self):
        """
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
        except AttributeError:
            return abort(401)
        try:
            decoded_token = jwt.decode(
                token,
                self.extensions.secret_key,
                algorithms="HS256"
            )
        except InvalidTokenError:
            return abort(401)

        try:
            entity = self.entity.get_entity_from_token(decoded_token)
            setattr(g, self.entity.get_entity_from_ext().__tablename__, entity)
        except ValueError:
            return abort(401)

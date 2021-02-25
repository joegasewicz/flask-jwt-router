"""
    Main class for routing
"""
from abc import ABC, abstractmethod
# pylint:disable=invalid-name
import logging
from flask import request, abort, g
from werkzeug.routing import RequestRedirect
from werkzeug.exceptions import MethodNotAllowed, NotFound
from jwt.exceptions import InvalidTokenError
import jwt


from ._entity import BaseEntity
from .oauth2.google import Google
from ._config import Config

logger = logging.getLogger()


class BaseRouting(ABC):
    # pylint:disable=missing-class-docstring
    @abstractmethod
    def before_middleware(self) -> None:
        # pylint:disable=missing-function-docstring
        pass


class Routing(BaseRouting):
    """
    :param app: Flask application instance
    :param config: :class:`~flask_jwt_router._config`
    :param entity: :class:`~flask_jwt_router._entity`
    """
    def __init__(self, app, config: Config, entity: BaseEntity, google: Google = None):
        self.app = app
        self.config = config
        self.logger = logger
        self.entity = entity
        self.google = google

    def _prefix_api_name(self, w_routes=None):
        """
        If the config has JWT_ROUTER_API_NAME defined then
        update each white listed route with an api name
        :example: "/user" -> "/api/v1/user"
        :param w_routes:
        :return List[str]:
        """
        api_name = self.config.api_name
        if not api_name:
            return w_routes
        # Prepend the api name to the white listed route
        named_white_routes = []
        for route_name in w_routes:
            verb, path = route_name
            named_white_routes.append((verb, f"{api_name}{path}"))
        return named_white_routes

    def _add_static_routes(self, path: str) -> bool:
        """
        Always allow /static/ in path and handle static_url_path from Flask **kwargs
        :param path:
        :return:
        """
        paths = path.split("/")
        defined_static = self.app.static_url_path[1:]
        if path == "favicon.ico" or\
                paths[1] == "static" or\
                paths[1] == defined_static:
            return True
        return False

    # pylint:disable=no-self-use
    def _handle_pre_flight(self, method: str) -> bool:
        """
        Handle pre-flight requests with any verb
        :param method
        :return: {bool}
        """
        if method == "OPTIONS":
            return True
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
            if len(r) > 0:
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
            if self._handle_pre_flight(method):
                return False
            if method == white_route[0] and path == white_route[1]:
                return False
            if method == white_route[0] and self._handle_query_params(white_route[1], path):
                return False
        return True

    def _does_route_exist(self, url: str, method: str) -> bool:
        adapter = self.app.url_map.bind('')
        try:
            adapter.match(url, method=method)
        except RequestRedirect as e:
            # recursively match redirects
            return self._does_route_exist(e.new_url, method)
        except (MethodNotAllowed, NotFound):
            # no match
            return False
        return True

    def before_middleware(self) -> None:
        """
        Handles ignored & whitelisted & static routes with api name
        If it's not static, ignored whitelisted then authorize
        :return: Callable or None
        """
        #pylint:disable=inconsistent-return-statements
        path = request.path
        is_static = self._add_static_routes(path)
        method = request.method
        if not is_static:
            # Handle ignored routes
            if self._does_route_exist(path, method):
                is_ignored = False
                ignored_routes = self.config.ignored_routes
                if len(ignored_routes) > 0:
                    is_ignored = not self._allow_public_routes(ignored_routes)
                if not is_ignored:
                    white_routes = self._prefix_api_name(self.config.whitelist_routes)
                    not_whitelist = self._allow_public_routes(white_routes)
                    if not_whitelist:
                        self.entity.clean_up()
                        self._handle_token()

    def _handle_token(self):
        """
        Checks the headers contain a Bearer string OR params.
        Checks to see that the route is white listed.
        :return None:
        """
        entity = None
        try:
            if request.args.get("auth"):
                token = request.args.get("auth")
            elif request.headers.get("X-Auth-Token") is not None and self.google:
                bearer = request.headers.get("X-Auth-Token")
                token = bearer.split("Bearer ")[1]
                try:
                    if self.google.test_metadata:
                        email, entity = self.google._update_test_metadata(token)
                    else:
                        # Currently token refreshing is not supported, so pass the current token through
                        auth_results = self.google.authorize(token)
                        email = auth_results["email"]
                    self.entity.oauth_entity_key = self.config.oauth_entity
                    if not entity:
                        entity = self.entity.get_entity_from_token_or_tablename(
                            tablename=self.google.tablename,
                            email_value=email,
                        )
                        setattr(g, self.entity.get_entity_from_ext().__tablename__, entity)
                    else:
                        setattr(g, entity.__tablename__, entity)
                    setattr(g, "access_token", token)
                    # Clean up google test util
                    self.google.tear_down()
                    return None
                except InvalidTokenError:
                    return abort(401)
                except AttributeError:
                    return abort(401)
                except TypeError:
                    # This is raised from auth_results["email"] not present
                    abort(401)
            else:
                # Sometimes a developer may define the auth field name as Bearer or Basic
                auth_header = request.headers.get("Authorization")
                if not auth_header:
                    abort(401)
                if "Bearer " in auth_header:
                    token = auth_header.split("Bearer ")[1]
                elif "Basic " in auth_header:
                    token = auth_header.split("Basic ")[1]
        except AttributeError:
            return abort(401)
        try:
            decoded_token = jwt.decode(
                token,
                self.config.secret_key,
                algorithms="HS256"
            )
        except InvalidTokenError:
            return abort(401)
        try:
            self.entity_key = self.config.entity_key
            entity = self.entity.get_entity_from_token_or_tablename(decoded_token)
            setattr(g, self.entity.get_entity_from_ext().__tablename__, entity)
            return None
        except ValueError:
            return abort(401)

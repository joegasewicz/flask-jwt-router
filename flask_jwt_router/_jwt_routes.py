"""
    Public class JwtRoutes

    The main public API for flask-jwt-router with methods to
    handle JSON web tokens.

"""
from ._jwt_router import FlaskJWTRouter
from ._authentication import JWTAuthStrategy


class JwtRoutes(FlaskJWTRouter):
    """
    :param: app
    """
    def __int__(self):
        super(JwtRoutes, self).__init__()
        self.auth = JWTAuthStrategy()

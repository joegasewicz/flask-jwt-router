"""
    Public class JwtRoutes

    The main public API for flask-jwt-router with methods to
    handle JSON web tokens.


"""
from flask_jwt_router._jwt_router import FlaskJWTRouter
from flask_jwt_router._authentication import JWTAuthStrategy, SSHAuthStrategy


class JwtRoutes(FlaskJWTRouter):

    def __int__(self):
        super(JwtRoutes, self).__init__()
        self.auth = JWTAuthStrategy()


class SshRoutes(FlaskJWTRouter):

    def __int__(self):
        super(SshRoutes, self).__init__()
        self.auth = SSHAuthStrategy()

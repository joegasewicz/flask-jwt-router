"""
    Public class JwtRoutes

    The main public API for flask-jwt-router with methods to
    handle JSON web tokens.

    flask-JWT-Routes provides the following:
    -  Out of the box authentication with JSON Web tokens
    -  White list routes
    -  Optional Authenticated entity available on flask's g object

    This pkg creates JwtRouter objects with specific behaviour
    based on the cryptographic signing Algorithm.

    ..

    Quick Start
    ===========

    -----------
    Installation::

       pip install flask-jwt-router

    Wrap your Flask app::

       from flask_jwt_router import JwtRoutes
       app = Flask(__name__)
       JwtRoutes(app)

    White list Routes::

       app.config["WHITE_LIST_ROUTES"] = [
           ("POST", "/register"),
       ]

       @app.route("/register", methods=["POST"])
       def register():
           return "I don't need authorizing!"

    ..

"""
from ._jwt_router import FlaskJWTRouter
from ._authentication import JWTAuthStrategy


class JwtRoutes(FlaskJWTRouter):
    """
    :param: app
    """
    def __init__(self, app=None, **kwargs):
        super(JwtRoutes, self).__init__(app, **kwargs)
        self.auth = JWTAuthStrategy()

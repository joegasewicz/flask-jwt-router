"""
    flask-JWT-Routes provides the following:
    -  Out of the box authentication with JSON Web tokens
    -  White list routes
    -  Optional Authenticated entity available on flask's g object

    This pkg creates JwtRouter objects with specific behaviour
    based on the cryptographic signing Algorithm.

    Public API:

    extensions:

    SECRET_KEY
    ENTITY_KEY
    JWT_ROUTER_API_NAME
    WHITE_LIST_ROUTES
    IGNORED_ROUTES


    from flask_jwt_router import JwtRoutes

    jwt_routes = JwtRoutes(app, entity_model=UserModel)

    jwt_routes.init_app(app)
    jwt_routes.register_entity(entity_id=1)
    jwt_routes.update_entity(entity_id=1)

"""

from ._jwt_routes import JwtRoutes


if __name__ == "__main__":
    pass

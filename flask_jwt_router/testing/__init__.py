"""

jwt_routes = JwtRoutes(app, strategies=[Google])


class BaseJwtRoutes:
    pass

class JwtRoutes(BaseJwtRoutes):
    pass



# Usage:
if E2E_TESTS == True:

    class TestJwtRoutes(TestRouterMixin, BaseJwtRoutes):
        pass

    jwt_routes = TestJwtRoutes(app, strategies=[GoogleTest])
else:
    jwt_routes = JwtRoutes(app, strategies=[Google])
"""
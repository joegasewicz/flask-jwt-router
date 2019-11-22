from flask_jwt_router._jwt_routes import JwtRoutes


class TestExtension:


    def test_config(self):
        IGNORED_ROUTES = [
            ("GET", "/"),
            ("GET", "/ignore"),
        ]
        WHITE_LIST_ROUTES = [
            ("GET", "/test"),
        ]
        class App:
            config = {
                "IGNORED_ROUTES": IGNORED_ROUTES,
                "WHITE_LIST_ROUTES": WHITE_LIST_ROUTES,
            }
            def before_request(self, t):
                pass
        flask_jwt_router = JwtRoutes(App())
        assert flask_jwt_router.extensions.ignored_routes == IGNORED_ROUTES
        assert flask_jwt_router.extensions.whitelist_routes == WHITE_LIST_ROUTES
        flask_jwt = JwtRoutes()
        flask_jwt.init_app(App())
        assert flask_jwt.extensions.ignored_routes == IGNORED_ROUTES
        assert flask_jwt.extensions.whitelist_routes == WHITE_LIST_ROUTES



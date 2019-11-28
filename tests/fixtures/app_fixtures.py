import pytest
from flask import Flask, jsonify
from flask_jwt_router._jwt_routes import JwtRoutes
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
jwt_routes = JwtRoutes()

@app.route("/test", methods=["GET"])
def test_one():
    return "/test"


@pytest.fixture(scope="function")
def jwt_router_client(request):
    app.config = {**app.config, **request.param}
    app.config["TESTING"] = True
    jwt_routes.init_app(app)
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield client

    ctx.pop()





@pytest.fixture
def test_client_static():
    flask_app_static = Flask(__name__, static_folder="static_copy")
    flask_app_static.config["WHITE_LIST_ROUTES"] = [("GET", "/anything")]
    JwtRoutes(flask_app_static)
    static_client = flask_app_static.test_client()
    ctx = flask_app_static.app_context()
    ctx.push()
    yield static_client
    ctx.pop()

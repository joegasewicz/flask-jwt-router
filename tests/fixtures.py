import pytest
from flask import Flask
from flask_jwt_router.JwtRoutes import JwtRoutes

app = Flask(__name__)


@app.route("/test", methods=["GET"])
def test_one():
    return "/test"


@pytest.fixture(scope="function")
def jwt_router_client(request):
    app.config = {**app.config, **request.param}
    JwtRoutes(app)
    app.config["TESTING"] = True
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield client

    ctx.pop()


flask_app = Flask(__name__)


@flask_app.route("/api/v1/test", methods=["GET"])
def test_two():
    return "/test"


@pytest.fixture(scope='module')
def test_client():
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()


@pytest.fixture(scope='module')
def test_client_static():
    flask_app_static = Flask(__name__, static_folder="static_copy")
    testing_client = flask_app_static.test_client()
    ctx = flask_app_static.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()



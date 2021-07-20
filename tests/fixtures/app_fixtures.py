import pytest
from flask import Flask, jsonify, g
from flask_jwt_router import JwtRoutes, Google, GoogleTestUtil


app = Flask(__name__, )
jwt_routes = JwtRoutes()

@app.route("/test", methods=["GET"])
def test_one():
    return "/test"



@app.route("/api/v1/test_google_oauth", methods=["GET"])
def request_google_oauth():
    oauth_tablename = g.oauth_tablename
    return {
        "email": oauth_tablename.email,
    }, 200


@pytest.fixture
def jwt_router_client(request):
    if hasattr(request, "param"):
        param = request.param
    else:
        param = {}
    app.config = {**app.config, **param}
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "__TEST_SECRET__"
    google_oauth = {
        "client_id": "<CLIENT_ID>",
        "client_secret": "<CLIENT_SECRET>",
        "redirect_uri": "http://localhost:3000",
        "tablename": "oauth_tablename",
        "email_field": "email",
        "expires_in": 3600,
    }
    jwt_routes.init_app(app, google_oauth=google_oauth, strategies=[GoogleTestUtil])
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield client
    ctx.pop()


@pytest.fixture
def test_client_static():
    flask_app_static = Flask(__name__, static_folder="static_copy")
    flask_app_static.config["WHITE_LIST_ROUTES"] = [("GET", "/anything")]
    flask_app_static.config["SECRET_KEY"] = "__TEST_SECRET__"
    JwtRoutes(flask_app_static)
    static_client = flask_app_static.test_client()
    ctx = flask_app_static.app_context()
    ctx.push()
    yield static_client
    ctx.pop()

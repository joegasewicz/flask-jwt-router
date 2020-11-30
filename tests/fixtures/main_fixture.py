import pytest
from flask import Flask, jsonify, g, request
from flask_jwt_router._jwt_routes import JwtRoutes
from flask_sqlalchemy import SQLAlchemy

flask_app = Flask(__name__)
jwt_routes = JwtRoutes()
db = SQLAlchemy()


@flask_app.route("/api/v1/test", methods=["GET"])
def test_two():
    return "/test"


@flask_app.route("/api/v1/bananas/sub", methods=["GET"])
def test_sub():
    return jsonify({"data": "sub"})


@flask_app.route("/api/v1/test/sub_two", methods=["GET"])
def test_sub_two():
    return jsonify({"data": "sub2"})


@flask_app.route("/api/v1/apples/sub/<int:user_id>", methods=["PUT"])
def test_three(user_id=1):
    return jsonify({"data": user_id})


@flask_app.route("/ignore", methods=["GET"])
def test_sub_four():
    return jsonify({"data": "ignore"})


@flask_app.route("/", methods=["GET"])
def test_sub_five():
    return jsonify({"data": "/"})


@flask_app.route("/api/v1/test_entity", methods=["POST"])
def test_entity():
    from tests.fixtures.models import TeacherModel
    teacher = TeacherModel(name="joe")
    teacher.save()
    token = jwt_routes.create_token(entity_id=1, table_name="teachers")
    return jsonify({
        "token": token,
    })


@flask_app.route("/api/v1/test_entity", methods=["GET"])
def test_entity_two():
    token = jwt_routes.update_token(entity_id=1)
    return jsonify({
        "token": token,
        "data": {
            "teacher_id": g.teachers.teacher_id,
            "name": g.teachers.name,
        }
    })


@flask_app.route("/api/v1/google_login", methods=["POST"])
def google_login():
    data = jwt_routes.google.oauth_login(request)
    return data, 200


@flask_app.route("/api/v1/mock_google_exchange", methods=["POST"])
def google_exchange():
    return {
        "data": "hello!"
    }


@pytest.fixture(scope='module')
def test_client():
    flask_app.config["SECRET_KEY"] = "__TEST_SECRET__"
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    flask_app.config["JWT_ROUTER_API_NAME"] = "/api/v1"
    flask_app.config["WHITE_LIST_ROUTES"] = [
        ("GET", "/test"),
        ("POST", "/test_entity"),
        ("GET", "/bananas/sub"),
        ("PUT", "/apples/sub/<int:user_id>"),
    ]
    flask_app.config["IGNORED_ROUTES"] = [
        ("GET", "/"),
        ("GET", "/ignore"),
    ]

    from tests.fixtures.models import TeacherModel
    flask_app.config["ENTITY_MODELS"] = [TeacherModel]

    google_oauth = {
        "client_id": "<CLIENT_ID>",
        "client_secret": "<CLIENT_SECRET>",
        "redirect_uri": "http://localhost:3000",
        "tablename": "oauth_tablename",
        "email_field": "email",
        "expires_in": 3600,
    }
    jwt_routes.init_app(flask_app, google_oauth=google_oauth)
    db.init_app(flask_app)

    with flask_app.app_context():
        db.create_all()

    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()

    ctx.push()

    yield testing_client

    with flask_app.app_context():
        db.session.remove()
        db.drop_all()

    ctx.pop()

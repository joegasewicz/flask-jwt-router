import pytest
from flask import Flask, jsonify, g
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
    token = jwt_routes.register_entity(entity_id=1, entity_type="teachers")
    return jsonify({
        "token": token,
    })


@flask_app.route("/api/v1/test_entity", methods=["GET"])
def test_entity_two():
    token = jwt_routes.update_entity(entity_id=1)
    keys = g.teachers.__table__.columns
    values = g.teachers.__table__.columns._data.values()
    print("keys", keys)
    print("values ----> ", values)
    return jsonify({
        "token": token,
        "data": {
            "keys": keys,
            "values": values,
        }
    })


@pytest.fixture(scope='module')
def test_client():

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    flask_app.config["JWT_ROUTER_API_NAME"] = "/api/v1"
    flask_app.config["WHITE_LIST_ROUTES"] = [
        ("GET", "/test"),
        ("POST", "/test_entity"),
        ("GET", "/bananas/sub"),
        ("PUT", "/apples/sub/<int:user_id>")
    ]
    flask_app.config["IGNORED_ROUTES"] = [
        ("GET", "/"),
        ("GET", "/ignore"),
    ]

    from tests.fixtures.models import TeacherModel
    flask_app.config["ENTITY_MODELS"] = [TeacherModel]

    jwt_routes.init_app(flask_app)
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

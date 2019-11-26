[![PyPI version](https://badge.fury.io/py/flask-jwt-router.svg)](https://badge.fury.io/py/flask-jwt-router)
[![Build Status](https://travis-ci.org/joegasewicz/Flask-JWT-Router.svg?branch=master)](https://travis-ci.org/joegasewicz/Flask-JWT-Router)
[![codecov](https://codecov.io/gh/joegasewicz/Flask-JWT-Router/branch/master/graph/badge.svg)](https://codecov.io/gh/joegasewicz/Flask-JWT-Router)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c15de26af47d48448392eaa5e0e41bcf)](https://www.codacy.com/manual/joegasewicz/Flask-JWT-Router?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=joegasewicz/Flask-JWT-Router&amp;utm_campaign=Badge_Grade)
[![Documentation Status](https://readthedocs.org/projects/flask-jwt-router/badge/?version=latest)](https://flask-jwt-router.readthedocs.io/en/latest/?badge=latest)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flask-jwt-router)
![PyPI - License](https://img.shields.io/pypi/l/flask-jwt-router?color=pink)

![Greenprint](logo.png?raw=true "Title")

# Flask JWT Router

Flask JWT Router is a Python library that adds authorised routes to a Flask app.

Read the Documentation here: [Flask-JWT-Router](https://flask-jwt-router.readthedocs.io/en/latest/) 

## Installation

```bash
pip install flask-jwt-router
```

## Basic Usage
 ```python
from flask import Flask
from flask_jwt_router import JwtRoutes

app = Flask(__name__)

JwtRoutes(app)

# If you're using the Flask factory pattern:
jwt_routes = JwtRoutes()  # Example with *entity_model - see below

def create_app(config):
    ...
    jwt_routes.init_app(app)

```

## Whitelist Routes
```python
app.config["WHITE_LIST_ROUTES"] = [
    ("POST", "/register"),
]

@app.route("/register", methods=["POST"])
def register():
    return "I don't need authorizing!"
```

## Prefix your api name to whitelisted routes
```python
    # All routes will
app.config["JWT_ROUTER_API_NAME"] = "/api/v1"
app.config["WHITE_LIST_ROUTES"] = [
    ("POST", "/register"),
]

@app.route("/api/v1/register", methods=["POST"])
def register():
    return "I don't need authorizing!"
   
```

## Bypass Flask-JWT-Router on specified routes
```python
    # Define homepage template routes for example on JWT_IGNORE_ROUTES 
    # & still get to use the api name on request handlers returning resources
    app.config["IGNORED_ROUTES"] = [
        ("GET", "/")
    ]
```

## Declare an entity model
```python
# Create your entity model (example uses Flask-SqlAlchemy)
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
# You can define the primary key name with `ENTITY_KEY` on Flask's config
app.config["ENTITY_KEY"] = "user_id"
# (`id` is used by default)
JwtRoutes(app)

# You can also specify a list of entity model classes

app.config["ENTITY_MODELS"] = [ UserModel, TeacherModel, ...etc ]

```

## Authorization
```python
from your_app import jwt_routes

# white list the routes
app.config["WHITE_LIST_ROUTES"] = [
    ("POST", "/register"),
    ("POST", "/login"),
]

@app.route("/register", methods=["POST"])
def register():
    """I'm registering a new user & returning a token!"""
    return jsonify({
        "token": jwt_routes.register_entity(entity_id=1, entity_type='users')
    })

@app.route("/login", methods=["POST"])
def login():
    """I'm authorized & updating my token!"""
    return jsonify({
        "token": jwt_routes.update_entity(entity_id=1)
    })
```

*Warning: The `entity_type` must be the same as your tablename or `__tablename__` attribute's value.
(With SqlAlchemy, you can define a `__tablename__` attribute directly or else
the name is derived from your entity’s database table name).

# Create & update Tokens on Routes
Create a new entity & return a new token
```python
@app.route("/register", methods=["POST"])
    def register():
        user_data = request.get_json()
        try:
            user = UserModel(**user_data)
            user.create_user() # your entity creation logic

            # Here we pass the id as a kwarg to `register_entity`
            token: str = jwt_routes.register_entity(entity_id=user.id, entity_type="users")

            # Now we can return a new token!
            return {
                "message": "User successfully created.",
                "token": str(token),  # casting is optional
            }, 200
```
Access entity on Flask's global context
```python
    from app import app, jwt_routes

    # Example uses Marshmallow to serialize entity object
    class EntitySchema(Schema):
        id = fields.Integer()
        name = fields.String()

    @app.route("/login", methods=["GET"])
    def login():
        user_data = g.get("user")
        try:
            user_dumped = UserSchema().dump(user_data)
        except ValidationError as _:
           return {
                       "error": "User requested does not exist."
                   }, 401
        return {
            "data": user_dumped,
            "token": jwt_routes.update_entity(entity_id=user_data.id),
        }, 200
        
```
If you are handling a request with a token in the headers you can call::
```python
    jwt_routes.update_entity(entity_id=user_data.id)
```

If you are handling a request without a token in the headers you can call::

```python
    jwt_routes.register_entity(entity_id=user_data.id, entity_type="users")
```


An Example configuration for registering & logging in users of different types:
```python
    app.config["IGNORED_ROUTES"] = [("GET", "/")]
    app.config["JWT_ROUTER_API_NAME"] = "/api/v1"
    app.config["WHITE_LIST_ROUTES"] = [
        ("POST", "/auth/user"), ("POST", "/auth/user/login"),
        ("POST", "/auth/teacher"), ("POST", "/auth/teacher/login"),
    ]
    app.config["ENTITY_MODELS"] = [UserModel, TeacherModel]
```
## Authors

* **joegasewicz** - *Initial work* - [@joegasewicz](https://twitter.com/joegasewicz)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

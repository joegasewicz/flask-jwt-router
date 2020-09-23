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

This library is in a Beta stage.

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
# You are required to always set a unique SECRET_KEY for your app
app.config["SECRET_KEY"] = "your_app_secret_key"

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
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
# You can define the primary key name with `ENTITY_KEY` on Flask's config
app.config["ENTITY_KEY"] = "user_id"

# (`id` is used by default)
JwtRoutes(app, entity_models=[UserModel, TeacherModel, ...etc])

# Or pass later with `init_app`
def create_app(config):
    ...
    jwt_routes.init_app(app, entity_models=[UserModel, TeacherModel, ...etc])

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
        "token": jwt_routes.create_token(entity_id=1, table_name='users')
    })

@app.route("/login", methods=["POST"])
def login():
    """I'm authorized & updating my token!"""
    return jsonify({
        "token": jwt_routes.update_token(entity_id=1)
    })
```

*Warning: The `table_name` must be the same as your tablename or `__tablename__` attribute's value.
(With SqlAlchemy, you can define a `__tablename__` attribute directly or else
the name is derived from your entity’s database table name).

## Setting the Token Expire Duration
There are two ways to set the expire duration of the JWT.

from your app config
```python
        # Set the token expire duration to 7 days
        app.config["JWT_EXPIRE_DAYS"] = 7
```
calling the `set_exp`
```python

        # Set the token expire duration to 14 days
        jwt_routes = JwtRoutes()
        # jwt_routes.init_app( ...etc
        jwt_routes.set_exp(expire_days=14)
```
By default the expire duration is set to 30 days

## Create & update Tokens on Routes
Create a new entity & return a new token
```python
@app.route("/register", methods=["POST"])
    def register():
        user_data = request.get_json()
        try:
            user = UserModel(**user_data)
            user.create_user() # your entity creation logic

            # Here we pass the id as a kwarg to `create_token`
            token: str = jwt_routes.create_token(entity_id=user.id, table_name="users")

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
        user_data = g.get("users") # This is your SqlAlchemy `__tablename__` or the default name.
        try:
            user_dumped = UserSchema().dump(user_data)
        except ValidationError as _:
           return {
                       "error": "User requested does not exist."
                   }, 401
        return {
            "data": user_dumped,
            "token": jwt_routes.update_token(entity_id=user_data.id),
        }, 200
        
```
If you are handling a request with a token in the headers you can call::
```python
    jwt_routes.update_token(entity_id=user_data.id)
```

If you are handling a request without a token in the headers you can call::

```python
    jwt_routes.create_token(entity_id=user_data.id, table_name="users")
```

An Example configuration for registering & logging in users of different types:
```python
    app.config["IGNORED_ROUTES"] = [("GET", "/")]
    app.config["JWT_ROUTER_API_NAME"] = "/api/v1"
    app.config["WHITE_LIST_ROUTES"] = [
        ("POST", "/auth/user"), ("POST", "/auth/user/login"),
        ("POST", "/auth/teacher"), ("POST", "/auth/teacher/login"),
    ]
    
    # Optionally, you can pass your models to Flask's config:
    app.config["ENTITY_MODELS"] = [ UserModel, TeacherModel, ...etc ]
```

## JSON Web Token setup
To send the JSON web token from your front end, you will need to pass a `Bearer` string in your authorization header.
For example:
```javascript
    fetch(url, {
        headers: {
            Authorization: "Bearer <my_token>",
        }
    })
```
### Routing without headers
If you require calling a resource without passing headers, then you can use the ``auth`` query param (useful when streaming video files):
```python
    url = "http://example.com/cars?auth=my_token"
```


## Authors

* **joegasewicz** - *Initial work* - [@joegasewicz](https://twitter.com/joegasewicz)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

Make sure you have Python versions: `3.6`,  `3.7`,  `3.8`
Then run:
```python
    tox
```

To check the docs look good locally you can run:
```bash
    make html
```

## License
[MIT](https://choosealicense.com/licenses/mit/)

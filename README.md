# Flask JWT Router

Flask JWT Router is a Python library that adds authorised routes to a Flask app.

## Installation

```bash
pip install flask-jwt-router
```

## Basic Usage
 ```python
from flask import Flask
from flaskJWTRoutes import JwtRoutes

app = Flask(__name__)

JwtRoutes(app)

```

## White list Routes
```python
app.config["WHITE_LIST_ROUTES"] = [
    ("POST", "/register"),
]

@app.route("/register", methods=["POST"])
def register():
    return "I don't need authorizing!"
```

## Declare an entity model
```python
# Create your entity model (example uses Flask-SqlAlchemy)
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
# You can define the primary key name with `entity_key`
# (`id` is used by default)
JwtRoutes(app, entity_model=UserModel, entity_key="user_id")

```

## Authorization
```python
from flaskJWTRoutes.flask_jwt_routes import RouteHelpers
rh = RouteHelpers(app)

@app.route("/register", methods=["POST"])
def register():
    """I'm registering a new user & returning a token!"""
    return jsonify({
        "token": rh.register_entity(entity_id=1)
    })

@app.route("/login", methods=["POST"])
def login():
    """I'm authorized & updating my token!"""
    return jsonify({
        "token": rh.update_entity(entity_id=1)
    })
```

# Access your Entity flask's global context
```python
# Example uses Marshmallow to serialize entity object
class EntitySchema(Schema):
    id = fields.Integer()
    name = fields.String()

@app.route("/user", methods=["GET"])
def get_user():
    """I was authorized & i have a user!"""
    entity = EntitySchema().dumps(g.entity).data
    return jsonify({
        "entity": entity
    })

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
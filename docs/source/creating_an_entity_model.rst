Creating An Entity Model
========================

In this example we will use SQLAlchemy as our ORM library.

First lets import all the dependencies::

    from flask import Flask, jsonify, g
    from flask_sqlalchemy import SQLAlchemy
    from flask_jwt_router import JwtRoutes, RouteHelpers

Create a flask instance::

    app = Flask(__name__)

Create an SQLAlchmemy UserModel class passing the db instance::

    db = SQLAlchemy(app)

    class UserModel(db.Model):
        user_id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String)

Pass Flask's application instance as the first argument & then the UserModel class::

    JwtRoutes(app, entity_model=UserModel)

    or with Flask's factory pattern:
    jwt_routes = JwtRoutes(entity_model=UserModel)
    ...
    jwt_routes.init_app(app)

If the `UserModel` has a primary key other than `id`, we can declare the name::

    app.config["ENTITY_KEY"] = "user_id"


We can now access the entity on any authenticated route.

To access the entity we created above (in this case the user object), we use Flask's built in global context - `g`.

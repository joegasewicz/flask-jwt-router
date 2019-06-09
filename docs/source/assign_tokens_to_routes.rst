Assign Tokens To Routes
=======================

To return a JWT token from any route, we first need import the FlaskJwtRouter `RouteHelpers` class::

    from flask_jwt_router import RouteHelpers

To use `RouteHelpers`, create a single instance, passing in Flasks application instance::

    rh = RouteHelpers(app)

We can register a new user & return a token::

    user = UserModel(name="John Doe")
    token = rh.register_entity(entity_id=user.id)
    print(token)  # "eyJ0eXAiO...

Now when user `John Doe` wants to login, we can also update his token and return it back to him::

    user = db.query.filter_by(id=1).one()
    token = rh.update_entity(entity_id=user.id)
    print(token)  # "eyJ0eXAiO..."

If the `UserModel` primary key isn't `id`, we can declare it in Flask's config object::

    app.config["ENTITY_KEY"] = "user_id"


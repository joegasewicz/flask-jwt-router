Getting Started
===============

Installation::

   pip install flask-jwt-router

Wrap your Flask app::

   from flask import Flask
   from flask_jwt_router import JwtRoutes
   app = Flask(__name__)
   JwtRoutes(app)

White list Routes::

   app.config["WHITE_LIST_ROUTES"] = [
       ("POST", "/register"),
   ]

   @app.route("/register", methods=["POST"])
   def register():
       return "I don't need authorizing!"

..

Authorizing Routes::

    from flask_jwt_router import RouteHelpers
    rh = RouteHelpers(app)

    # white list the routes
    app.config["WHITE_LIST_ROUTES"] = [
        ("POST", "/register"),
        ("POST", "/login"),
    ]

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

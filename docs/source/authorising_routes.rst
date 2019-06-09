Authorising Routes
==================


To create a list of paths in your Flask app that are unauthorised, create a list of tuple pairs,
with the first item being a verb::

    white_list = [
       ("GET", "/cats"),
       ("POST", "/dogs"),
       ("PUT", "/fruit"),
       ("DELETE", "/clouds"),
   ]

Then pass the list to Flask's `WHITE_LIST_ROUTES` application config object::

    app.config["WHITE_LIST_ROUTES"] = white_list

Any routes that match the `white_list` tuple pairs will bypass authentication checks::

    @app.route("/cats", methods=["GET"])
    def register():
        return "I don't need authorizing!"

    @app.route("/dogs", methods=["POST"])
    def register():
        return "I don't need authorizing!"

    @app.route("/fruit", methods=["PUT])
    def register():
        return "I don't need authorizing!"

    @app.route("/clouds", methods=["DELETE"])
    def register():
        return "I don't need authorizing!"


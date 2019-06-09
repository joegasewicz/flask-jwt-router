Flask JWT Router
============================================

.. toctree::
   :maxdepth: 2

   getting_started
   contents


flask-JWT-Routes provides the following
+++++++++++++++++++++++++++++++++++++++
* Out of the box authentication with JSON Web tokens
* White list routes
* Optional Authenticated entity available on flask's g object

..

Quick Start
-----------
Installation::

   pip install flask-jwt-router

Wrap your Flask app::

   from flaskJWTRoutes import JwtRoutes
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

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

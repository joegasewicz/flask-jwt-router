.. Flask JWT Router documentation master file, created by
   sphinx-quickstart on Sat Nov 23 00:00:09 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Flask JWT Router's documentation!
============================================


.. toctree::
   :maxdepth: 2

   authentication
   entity
   extensions
   jwt_router
   jwt_routes
   routing


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

* :ref:`search`

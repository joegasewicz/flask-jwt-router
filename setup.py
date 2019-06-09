from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='flask-jwt-router',
    version='0.0.1',
    description='Flask JWT Router is a Python library that adds authorised routes to a Flask app',
    packages=["flask_jwt_routes"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joegasewicz/Flask-JWT-Router",
    author="Joe Gasewicz",
    author_email="joegasewicz@gmail.com"
)

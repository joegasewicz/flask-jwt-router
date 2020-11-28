class RequestAttributeError(Exception):
    message = "Did you mean to pass Flask's request to jwt_router.google.oauth_login()?" \
              "See https://flask-jwt-router.readthedocs.io/en/latest/"

    def __init__(self, err=""):
        super(RequestAttributeError, self).__init__(f"{err}\n{self.message}")

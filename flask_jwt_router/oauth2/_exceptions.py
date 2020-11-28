class RequestAttributeError(Exception):
    message = "Did you mean to pass Flask's request to jwt_router.google.oauth_login()?" \
              "See https://flask-jwt-router.readthedocs.io/en/latest/"

    def __init__(self, err=""):
        super(RequestAttributeError, self).__init__(f"{err}\n{self.message}")


class ClientExchangeCodeError(Exception):
    message: str

    def __init__(self, client_url):
        super(ClientExchangeCodeError, self).__init__()
        self.message = f"Error in POST {client_url} from client - code value not in request body."

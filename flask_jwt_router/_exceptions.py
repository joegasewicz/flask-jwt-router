class AuthenticationError(Exception):
    message = "algorithm kwarg must be set to either HS256 or RS256"

    def __init__(self, err=""):
        super(AuthenticationError, self).__init__(f"{err}\n{self.message}")
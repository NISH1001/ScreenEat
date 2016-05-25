class AuthError(Exception):
    """Exception class related to authentication process for upload."""

    def __init__(self, code, message):
        self.message = str(code) + " " + message

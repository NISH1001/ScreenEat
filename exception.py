class Error(Exception):
    """Exception class to be inherited for user defined excpetions."""

    def __init__(self):
        self.message = "User defined error occured."

class AuthError(Error):
    """Exception class related to authentication process for upload."""

    def __init__(self, code, message):
        self.message = str(code) + " " + message

class ManualError(Error):
    """Exception class related to define less generic exceptions."""

    def __init__(self, message):
        self.message = message

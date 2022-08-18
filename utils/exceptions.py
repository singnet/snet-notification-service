class CustomException(Exception):
    error_message = "ERROR"
    status_code = 0

    def __init__(self, error_details):
        self.error_details = error_details


class BadRequestException(CustomException):
    error_message = "BAD_REQUEST"
    status_code = 400

    def __init__(self):
        super().__init__({})


EXCEPTIONS = (BadRequestException)

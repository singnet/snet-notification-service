from enum import Enum


class StatusCode:
    BAD_REQUEST = 400
    INTERNAL_SERVER_ERROR = 500
    CREATED = 201
    OK = 200


class ResponseStatus:
    FAILED = "failed"
    SUCCESS = "success"


class NotificationType(Enum):
    SUPPORT = "support"


BODY_HTMLS = {NotificationType.SUPPORT.value: """<html>
<head></head>
<body>
  <p>{}</p>
</body>
</html>
"""}

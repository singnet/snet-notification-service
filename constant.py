from enum import Enum


class SendEmail(Enum):
    FROM = "FROM"
    TO = "TO"
    REPLY_TO = "REPLY_TO"
    ATTACHMENT_DETAILS = "ATTACHMENT_DETAILS"
    S3_REGION_NAME = "S3_REGION_NAME"
    SES_REGION_NAME = "SES_REGION_NAME"
    TYPE = "TYPE"
    S3_BUCKET = "S3_BUCKET"
    S3_PATH = "S3_PATH"
    CONTEXT = "CONTEXT"
    TEMPLATE_NAME = "TEMPLATE_NAME"
    MESSAGE_TEMPLATE = "MESSAGE_TEMPLATE"
    SUBJECT = "SUBJECT"


class NotificationAlert(Enum):
    MESSAGE = "message"
    ERROR_TIME = "error_time"
    LOG_STREAM = "logStream"
    ENV = "env"
    LOG_EVENTS = "logEvents"
    ERROR_MESSAGE = "error_message"
    DATA = "data"
    AWS_LOGS = "awslogs"
    SUBSCRIPTION_FILTERS = "subscriptionFilters"
    LOG_GROUP = "logGroup"
    BUTTON_URL = "buttonUrl"
    LAMBDA = "lambda"
    TIMESTAMP = "timestamp"
    WEBHOOK_URL = "webhook_url"
    TEAM = 'team'
    SLACK = 'slack'
    IMAGE_URL = "imageUrl"
    BUTTON_NAME = "buttonName"


class NotificationResponse(Enum):
    logGroup = "Log Group"
    logStream = "Log Stream"
    error_time = "Error Time"
    env = "Env"
    error_message = "Error Message"

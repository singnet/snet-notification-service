import json
from common.logger import get_logger
from common.utils import generate_lambda_response
from common.constant import StatusCode
from application.notification_service import EmailNotificationService
from application.user_message_service import UserMessageService

logger = get_logger(__name__)


def send_notification(event, context):
    logger.info(f"Send notification event:: {event}")
    payload = json.loads(event["body"])
    try:
        response = EmailNotificationService(payload=payload).send_notification()
    except Exception as e:
        print(repr(e))
        return {"status": "failed"}
    return {"status": response}


def process_user_message(event, context):
    logger.info(f"Send notification event:: {event}")
    payload = json.loads(event["body"])
    try:
        response = UserMessageService().process_messages(payload)
    except Exception as e:
        print(repr(e))
        return {"status": "failed"}

    return generate_lambda_response(
        StatusCode.OK,
        {"status": "success", "data": response, "error": {}}, cors_enabled=True
    )

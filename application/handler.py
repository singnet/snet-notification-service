import json
from common.logger import get_logger
from application.service import EmailNotificationService

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

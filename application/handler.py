import json

from application.notification_service import EmailNotificationService
from application.service.email_service import send_email_with_attachment
from application.user_message_service import UserMessageService
from common.constant import BODY_HTMLS, NotificationType, StatusCode
from common.logger import get_logger
from common.utils import generate_lambda_response
from config import EMAIL_FOR_SENDING_NOTIFICATION

logger = get_logger(__name__)

SENDERS = {
    NotificationType.SUPPORT.value: EMAIL_FOR_SENDING_NOTIFICATION
}


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
        response = UserMessageService.process_messages(payload)
    except Exception as e:
        print(repr(e))
        return generate_lambda_response(
            StatusCode.OK,
            {"status": "failed", "data": {}, "error": {"code": 0, "message": "Failed to process user message.", "details": repr(e)}}, cors_enabled=True
        )

    return generate_lambda_response(
        StatusCode.OK,
        {"status": "success", "data": response, "error": {}}, cors_enabled=True
    )


def send_email(event, context):
    logger.info(f"Send email event:: {event}")
    payload = json.loads(event["body"], "{}")
    headers = {
        "Access-Control-Allow-Headers": "Access-Control-Allow-Origin,"
                                        "Content-Type, X-Amz-Date,"
                                        "Authorization, X-Api-Key,"
                                        "X-Amz-Security-Token",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST"
    }
    try:
        if not payload:
            raise Exception("The data was not transmitted or "
                            "was transmitted incorrectly.")
        recipient = payload["recipient"]
        if not recipient:
            raise Exception("The recipient wasn't transmitted.")
        message = payload["message"] if "message" in payload else ""
        attachment_urls = (payload["attachment_urls"] if "attachment_urls"
                           in payload else [])
        subject = (payload["subject"] if "subject"
                   in payload else "Error occurred")
        notification_type = (payload["notification_type"]
                             if "notification_type" in payload else "")
        body_html = BODY_HTMLS[notification_type].format(message)
        sender = SENDERS[notification_type]
        send_email_with_attachment(recipient, subject,
                                   body_html, sender,
                                   attachment_urls=attachment_urls)
    except Exception as e:
        logger.exception(e)
        return generate_lambda_response(
            StatusCode.OK,
            {"status": "failed",
             "data": {},
             "error": {"code": 0,
                       "message": "Failed to send email.",
                       "details": repr(e)}},
            headers=headers
        )

    return generate_lambda_response(
        status_code=StatusCode.OK,
        message={"status": "success", "data": {}, "error": {}},
        headers=headers
    )

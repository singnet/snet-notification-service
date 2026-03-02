import json

from application.notification_service import EmailNotificationService
from application.service.alert_service import MattermostProcessor
from application.service.email_service import send_email_with_attachment
from application.user_message_service import UserMessageService
from common.constant import BODY_HTMLS, StatusCode
from common.logger import get_logger
from common.utils import generate_lambda_response
from config import EMAIL_FOR_SENDING_NOTIFICATION_DEPRECATED_VERSION, RegisteredApplication

logger = get_logger(__name__)


def send_notification(event: dict, context):
    logger.info(f"Send notification event:: {event}")
    payload = json.loads(event["body"])
    try:
        response = EmailNotificationService(payload=payload).send_notification()
    except Exception as e:
        print(repr(e))
        return {"status": "failed"}
    return {"status": response}


def process_user_message(event: dict, context):
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


def send_email(event: dict, context):
    logger.info(f"Send email event:: {event}")
    body = event.get("body", "{}")
    payload = json.loads(body)
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
        source = payload.get("source")
        if source:
            # New version with source param in payload
            sender = RegisteredApplication[source]["senders"][notification_type]
        else:
            # Old version without source param for unknown services
            sender = EMAIL_FOR_SENDING_NOTIFICATION_DEPRECATED_VERSION

            # send message to MM to info
            alert_processor = MattermostProcessor()
            alert_processor.send(message="### :warning: Received a request to send an email "
                                         f"for a deprecated version.\nEvent: {event}\n")

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

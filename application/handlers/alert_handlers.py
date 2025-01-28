import json
import os
from http import HTTPStatus

from application.service.alert_service import convert_cw_to_event_format, get_data_from_event
from common.exception_handler import exception_handler
from common.logger import get_logger
from common.utils import generate_lambda_response, make_response_body
from utils.exceptions import EXCEPTIONS

logger = get_logger(__name__)
pause_notification = os.environ.get('PAUSE_NOTIFICATION', "no")


@exception_handler(logger=logger, EXCEPTIONS=EXCEPTIONS)
def send_notification_alert(event, context):
    logger.info("Started alerting for the request")
    payload = convert_cw_to_event_format(event)
    logger.info(f"Event={json.dumps(payload)}")
    if pause_notification.lower() == "yes":
        return generate_lambda_response(HTTPStatus.OK.value,
                                        make_response_body("failed", {"status": "Not processing"}, ""))

    response = get_data_from_event(payload)

    return generate_lambda_response(HTTPStatus.OK.value, make_response_body("success", response, ""))

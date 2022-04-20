import json

from config import RegisteredApplication, AllowedActions
from constant import SendEmail
from infrastructure.repositories.user_message_repo import UserMessageHistoryRepo
from templates.mail_templates import prepare_notification_email_message
from common.logger import get_logger
from common.boto_utils import BotoUtils
from config import NOTIFICATION_ARN, AWS_REGION

user_message_repo = UserMessageHistoryRepo()
boto_utils = BotoUtils(region_name=AWS_REGION)
logger = get_logger(__name__)
DEFAULT_SOURCE = "Anonymous"


class UserMessageService:
    def __init__(self):
        pass

    @staticmethod
    def validate_message_and_message_type(message, message_type):
        if len(message) and len(message_type):
            return True
        raise Exception("Mandatory fields message and message type can't be none.")

    @staticmethod
    def is_source_registered(source):
        if source in RegisteredApplication.keys():
            return True
        return False

    def process_messages(self, payload):
        message = payload.get("message", "")
        message_type = payload.get("message_type", "")
        source = payload.get("source", DEFAULT_SOURCE)
        name = payload.get("name", "")
        address = payload.get("address", "")
        email = payload.get("email", "")
        phone_no = payload.get("phone_no", "")
        subject = payload.get("subject", "")

        user_message_repo.add_message(source, name, address, email, phone_no, message_type, subject, message)

        if not UserMessageService.is_source_registered(source):
            return
        registered_actions = RegisteredApplication[source].keys()
        message_details = {"message_type": message_type, "name": name, "address": address, "email": email,
                           "phone_no": phone_no, "subject": subject, "message": message}
        UserMessageService.process_actions(source, registered_actions, message_details)
        return

    @staticmethod
    def process_actions(source, registered_actions, message_details):
        for action in registered_actions:
            if action == AllowedActions.EMAIL.value:
                email_details = prepare_notification_email_message(message_details)
                email_addresses = RegisteredApplication[source][action].get("email-addresses", [])
                UserMessageService.send_emails(email_addresses, email_details)
        return

    @staticmethod
    def send_emails(email_addresses, payload):
        for email_addresss in email_addresses:
            payload.update({
                "notification_type": "support",
                "recipient": email_addresss})
            payload = {"body": json.dumps(payload)}
            boto_utils.invoke_lambda(lambda_function_arn=NOTIFICATION_ARN, invocation_type="RequestResponse",
                                     payload=json.dumps(payload))
            logger.info(f"Mail sent to {email_addresss}")

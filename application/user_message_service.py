import json
import os
import re

from common.boto_utils import BotoUtils
from common.logger import get_logger
from config import AWS_REGION, RegisteredApplication, AllowedActions
from infrastructure.repositories.user_message_repo import UserMessageHistoryRepo
from templates.mail_templates import prepare_notification_email_message

SERVICE = os.getenv("SERVICE")
STAGE = os.getenv("STAGE")

user_message_repo = UserMessageHistoryRepo()
boto_utils = BotoUtils(region_name=AWS_REGION)
logger = get_logger(__name__)


class UserMessageService:
    def __init__(self):
        pass

    @staticmethod
    def validate_mandatory_fields(payload, fields):
        empty_fields = []
        for field in fields:
            if not payload.get(field):
                empty_fields.append(field)
        if empty_fields:
            raise Exception(f"Mandatory fields {', '.join(empty_fields)} can't be empty.")

    @staticmethod
    def validate_source(source):
        if not source:
            raise Exception("Mandatory field source can't be empty.")
        elif source not in RegisteredApplication.keys():
            raise Exception("Invalid source field")

    @classmethod
    def process_messages(cls, payload):
        message = payload.get("message", "")
        message_type = payload.get("message_type", "")
        source = payload.get("source", "")
        name = payload.get("name", "")
        address = payload.get("address", "")
        email = payload.get("email", "")
        phone_no = payload.get("phone_no", "")
        subject = payload.get("subject", "")
        priority = payload.get("priority", "")
        attachment_urls = payload.get("attachment_urls", [])
        details = payload.get("details", {})

        cls.validate_source(source)

        fields_to_check = ["email", "message", "message_type"]
        if source in ["DEVELOPER_PORTAL", "MARKETPLACE", "ASI_CHAIN_DOCS", "ASI_CHAIN_EXPLORER", "ASI_CHAIN_FAUCET", "ASI_CHAIN_WALLET", "ASI_CREATE"]:
            fields_to_check += ["name"]
        elif source == "BRIDGE":
            fields_to_check += ["address"]
        cls.validate_mandatory_fields(payload, fields_to_check)

        pattern = r"^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\\\".+\\\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"
        if not re.match(pattern, email):
            raise Exception("Invalid email")

        if (source in ["BRIDGE", "DEVELOPER_PORTAL", "UI_CONSTRUCTOR", "MARKETPLACE", "ASI_CHAIN_DOCS", "ASI_CHAIN_EXPLORER", "ASI_CHAIN_FAUCET", "ASI_CHAIN_WALLET"]
            and not message_type.lower() in ['question', 'bug', 'feedback']):
            raise Exception("Invalid message_type")

        if source in ["ASI_CREATE"]:
            if not message_type.lower() in ['question', 'bug', 'feedback', 'feature']:
                raise Exception("Invalid message_type")
            if not priority.lower() in ['low', 'middle', 'high']:
                raise Exception("Invalid priority")

        pattern_ethereum = r"^(0x[a-fA-F0-9]{40})$"
        pattern_cardano = r"^(addr1[a-z0-9]{98})$"

        if (source == "BRIDGE"
                and not re.match(pattern_cardano, address)
                and not re.match(pattern_ethereum, address)):
            raise Exception("Invalid address")

        if any(not isinstance(x, str) for x in details.values()):
            raise Exception("Values in details should be strings")

        if source == "UI_CONSTRUCTOR":
            for key in set(details.keys()) - {"org_id", "service_id", "endpoint"}:
                del details[key]

        user_message_repo.add_message(source, name, address, email, phone_no, message_type, subject, message)

        registered_actions = RegisteredApplication[source].keys()
        message_details = {"message_type": message_type, "name": name, "address": address, "email": email,
                           "phone_no": phone_no, "subject": subject, "message": message,
                           "attachment_urls": attachment_urls, "details": details}
        cls.process_actions(source, registered_actions, message_details, email)
        return

    @staticmethod
    def process_actions(source, registered_actions, message_details, email):
        email_sent_user_address = False
        for action in registered_actions:
            if action == AllowedActions.EMAIL.value:
                email_details = prepare_notification_email_message(message_details)
                email_addresses = list(RegisteredApplication[source][action].get("email-addresses", []))

                # Adding user address to the email addresses list
                if email and email_sent_user_address is False:
                    email_addresses.append(email)
                    email_sent_user_address = True

                email_addresses = list(set(email_addresses))
                UserMessageService.send_emails(email_addresses, email_details)
        return

    @staticmethod
    def send_emails(email_addresses, email_details):
        email_details.update({"notification_type": "support"})
        for email_addresss in email_addresses:
            email_details.update({"recipient": email_addresss})
            payload = {"body": json.dumps(email_details)}
            if not SERVICE or not STAGE:
                raise Exception("Service or Stage are missing")
            boto_utils.invoke_lambda(lambda_function_arn=f"{SERVICE}-{STAGE}-send_email", invocation_type="Event",
                                     payload=json.dumps(payload))
            logger.info(f"Mail sent to {email_addresss}")

DEFAULT_SOURCE = "Anonymous"

from config import RegisteredApplication, AllowedActions
from constant import SendEmail
from infrastructure.repositories.user_message_repo import UserMessageHistoryRepo
from application.notification_service import SlackNotificationService, EmailNotificationService

user_message_repo = UserMessageHistoryRepo()


class UserMessageService:
    def __init__(self):
        pass

    def validate_message_and_message_type(self, message, message_type):
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
        message_details = {"subject": subject, "message": message}
        UserMessageService.process_actions(source, registered_actions, message_details)
        return

    @staticmethod
    def process_actions(source, registered_actions, message_details):
        for action in registered_actions:
            if action == AllowedActions.EMAIL.value:
                email_details = {
                    SendEmail.SUBJECT.value: message_details.get("subject", ""),
                    SendEmail.CONTEXT.value: message_details.get("message", ""),
                }
                email_details = email_details.update(RegisteredApplication[source][action])
                EmailNotificationService(email_details).send_notification()
            if action == AllowedActions.SLACK.value:
                slack_details = RegisteredApplication[source][action]
                hostname, path, channel = slack_details["hostname"], slack_details["path"], slack_details["channel"]
                SlackNotificationService(hostname, path, channel).send_notification(message_details.get("message", ""))
        return

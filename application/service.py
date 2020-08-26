import boto3
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from domain.email import Email
from constant import SendEmail
from config import TEMPLATES
from common.logger import get_logger

logger = get_logger(__name__)


class EmailNotificationService:

    def __init__(self, payload):
        self.__email = Email(
            from_address=payload.get(SendEmail.FROM.value, None),
            to_address=payload.get(SendEmail.TO.value, None),
            reply_to_address=payload.get(SendEmail.REPLY_TO.value, None),
            subject=None,
            message_body=None,
            attachment_path=None
        )
        template_name, self.__email.subject = \
            self.get_template_details(message_template=payload.get(SendEmail.MESSAGE_TEMPLATE.value, None))
        self.__email.generate_message_body(
            template_name=template_name,
            context=payload.get(SendEmail.CONTEXT.value, {})
        )
        self.__email.attachment_path = self.get_attachment_details(
            attachment_details=payload.get(SendEmail.ATTACHMENT_DETAILS.value, None)
        )
        self.__ses_region_name = payload.get(SendEmail.SES_REGION_NAME.value, None)

    @staticmethod
    def get_template_details(message_template):
        template_details = TEMPLATES.get(message_template, None)
        return template_details.get(SendEmail.TEMPLATE_NAME.value, None), template_details.get(SendEmail.SUBJECT.value)

    @staticmethod
    def get_attachment_details(attachment_details):
        if bool(attachment_details):
            if attachment_details.get(SendEmail.TYPE.value, None) == "S3":
                path = attachment_details.get(SendEmail.S3_PATH.value, None)
                bucket = attachment_details.get(SendEmail.S3_BUCKET.value, None)
                region_name = attachment_details.get(SendEmail.S3_REGION_NAME.value, None)
                if bool(path) and bool(bucket) and bool(region_name):
                    filename = os.path.basename(path)
                    attachment_path = '/tmp/' + filename
                    boto3.client("s3", region_name=region_name).download_file(bucket, path, attachment_path)
                    return attachment_path
            raise Exception("Attachment is not valid.")
        return None

    def validate_parameters(self):
        if not bool(self.__email.from_address):
            raise Exception("From address is blank.")
        if not bool(self.__email.to_address):
            raise Exception("To address list is blank.")
        if not bool(self.__email.subject):
            raise Exception('Email subject is blank.')
        if not bool(self.__email.message_body):
            raise Exception('Email message body is blank.')
        if not bool(self.__ses_region_name):
            raise Exception('SES region name is blank.')

    def send_notification(self):
        self.validate_parameters()
        email = Email(
            from_address=self.__from_address,
            to_address=self.__to_address_list,
            reply_to_address=self.__from_address,
            subject=self.__subject,
            message_body=self.__message_body,
            attachment_path=self.__attachment_path
        )
        message = MIMEMultipart('mixed')
        message['Subject'] = email.subject
        message['From'] = email.from_address
        message['To'] = ', '.join(email.to_address)
        if bool(email.__reply_to):
            message.add_header('reply-to', email.reply_to)
        message_body = MIMEMultipart('alternative')
        htmlpart = MIMEText(email.message, 'html', "utf-8")
        message_body.attach(htmlpart)
        message.attach(message_body)
        if self.filepath:
            attachment = MIMEApplication(open(self.filepath, 'rb').read())
            attachment.add_header('Content-Disposition', 'Report', filename=os.path.basename(email.attachment_path))
            message.attach(attachment)

        client = boto3.client('ses', region_name=self.__ses_region_name)
        response = client.send_raw_email(
            Source=email.from_address,
            Destinations=email.to_address,
            RawMessage={
                'Data': message.as_string(),
            }
        )
        print(response)
        return "success"


class SMSNotificationService:
    def __init__(self):
        pass

    def send_notification(self):
        pass


class SlackNotificationService:
    def __init__(self):
        pass

    def send_notification(self):
        pass

from jinja2 import Environment, FileSystemLoader
from common.logger import get_logger

logger = get_logger(__name__)


class Email:
    def __init__(self, from_address, to_address, reply_to_address, subject, message_body, attachment_path):
        self.__from_address = from_address
        self.__to_address = to_address
        self.__reply_to_address = reply_to_address
        self.__subject = subject
        self.__message = message_body
        self.__attachment_path = attachment_path

    @property
    def from_address(self):
        return self.__from_address

    @property
    def to_address(self):
        return self.__to_address

    @property
    def reply_to_address(self):
        return self.__reply_to_address

    @property
    def subject(self):
        return self.__subject

    @subject.setter
    def subject(self, subject):
        self.__subject = subject

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, message):
        self.__message = message

    @property
    def attachment_path(self):
        return self.__attachment_path

    @attachment_path.setter
    def attachment_path(self, attachment_path):
        self.__attachment_path = attachment_path

    def generate_message_body(self, template_name, context):
        if not bool(template_name):
            raise Exception("Template name is blank.")
        context = context if bool(context) else {}
        file_loader = FileSystemLoader('templates')
        environment = Environment(loader=file_loader)
        try:
            template_name = environment.get_template(template_name)
        except Exception as e:
            logger.info(f"Error in fetching template:: {repr(e)}")
            raise Exception("Template name is not valid.")
        self.__message = template_name.render(context)

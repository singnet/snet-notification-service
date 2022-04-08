from enum import Enum

TEMPLATES = {
    "REJUVE_DATA_EXPORT": {
        "TEMPLATE_NAME": "rejuveDataExport",
        "SUBJECT": "Your Rejuve Data Export"
    },
    "SNET_WEBSITE_INFO": {
        "TEMPLATE_NAME": "snetWebsiteInfo",
        "SUBJECT": "Inquiry from the website"
    }
}
DB_DETAILS = {
    "driver": "mysql+pymysql",
    "host": "localhost",
    "user": "unittest_root",
    "password": "unittest_pwd",
    "name": "notification_unittest_db",
    "port": 3306
}


class AllowedActions(Enum):
    EMAIL = "EMAIL"
    SLACK = "SLACK"


RegisteredApplication = {
    "PUBLISHER_PORTAL": {
        AllowedActions.EMAIL.value: {
            "email-addresses": [],
            "template": ""
        },
        AllowedActions.SLACK.value: {
            "hostname": "",
            "path": ""
        }
    }
}

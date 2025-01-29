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
            "email-addresses": ["test@test.grr.la"],
            "template": ""
        }
    },
    "BRIDGE": {
        AllowedActions.EMAIL.value: {
            "email-addresses": ["test@test.grr.la"],
            "template": ""
        }
    },
    "TOKEN_TRANSFER": {
        AllowedActions.EMAIL.value: {
            "email-addresses": ["test@test.grr.la"],
            "template": ""
        }
    }
}
NOTIFICATION_ARN = ""
AWS_REGION = "us-east-1"

EMAIL_FOR_SENDING_NOTIFICATION = ""
S3_DOWNLOAD_API = {
    "HOST": "",
    "TOKEN": ""
}

ALERT_CONFIG = {
    "rt-v2": {
        "/aws/lambda/converterservices-rt-v2-": {
            "default": {
                "slack": [
                    {
                        "webhook_url": "",
                        "imageUrl": "https://d2adhoc2vrfpqj.cloudfront.net/2020/02/1zBSAFh5KIA72dmf1j9vfZQ.jpeg",
                        "buttonName": "Open Cloudwatch",
                        "buttonUrl": ""
                    }
                ]
            }
        }
    },
    "mt-v2": {
        "/aws/lambda/converterservices-mt-v2": {
            "default": {
                "slack": [
                    {
                        "webhook_url": "",
                        "imageUrl": "https://d2adhoc2vrfpqj.cloudfront.net/2020/02/1zBSAFh5KIA72dmf1j9vfZQ.jpeg",
                        "buttonName": "Open Cloudwatch",
                        "buttonUrl": ""
                    }
                ]
            }
        }
    }
}

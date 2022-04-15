import json
from unittest import TestCase
from application.handler import process_user_message


class TestProcessUserMessage(TestCase):
    def setUp(self):
        pass

    def test_process_user_message(self):
        event = {
            "body": json.dumps(
                {
                    "source": "PUBLISHER_PORTAL",
                    "name": "TestName",
                    "address": "0x",
                    "email": "test@test.com",
                    "phone_no": "+99 9876543210",
                    "message_type": "General",
                    "subject": "Test Subject",
                    "message": "Test Message"
                }
            )
        }
        response = process_user_message(event, context=None)
        assert (response["statusCode"] == 200)

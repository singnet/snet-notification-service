import json
from unittest import TestCase, mock
from unittest.mock import patch

from application.handlers.alert_handlers import send_notification_alert


class TestAlert(TestCase):

    def setUp(self):
        pass

    @mock.patch('application.service.alert_service.ALERT_CONFIG', {
        "default": {
            "/aws/lambda/": {
                "test": {
                    "slack": [
                        {
                            "webhook_url": "test",
                            "imageUrl": "https://d2adhoc2vrfpqj.cloudfront.net/2020/02/1zBSAFh5KIA72dmf1j9vfZQ.jpeg",
                            "buttonName": "Open Cloudwatch",
                            "buttonUrl": ""
                        }
                    ]
                }
            }
        }
    })
    @patch('application.service.alert_service.send_slack_message')
    def test_send_notification_alert(self, mock_send_team_message):
        event = {
            "awslogs": {
                "data": "H4sIAAAAAAAAAMXUW2vbMBQH8K8izB7jRZejW2APYUvLYJeH5GlNMIolJ6KObWylXSn97jtO1+0prGzd9mKMJI74/3yO77NDGAa3C6u7LmSz7N18NS8+LpbL+eUim2TtbRN6XDZacs6sNkooXK7b3WXfHjvcmbrbYVq7w9a7qWtcfZdiOeRd3/p8F1LetX2q2jq2+XUXcx+Si/XwWGGZ+uAOWIJTzqcUptxOr159mK8Wy9XGKMVtpUFa76BSpeXgDYjAlJVAyy2WGI7boexjl2LbXMQ6hX7IZldZCkPKNqcbFjehSePifRY9XiSU4YKD4QYMs4JqhQtcgAVQlgpmpWZCUcaYVMAZ49RKyrXEy1JEp+QOGJkpyfh4hGohJ09+WP7q/aeLz5t1GvPkFHJuV1TOJJ8Bfa0FfFmnqqzASCpzIajKAXSVuxBkvrWeBydYJUq5Tm/RJQVPHGnCLemDH/axSqRsmyaUY1pStT3BaKHv+jgEEj3ZOh1cyb0F7SAwvcVIQCFwp7iqzJa4xpPSlXusGxtCHr/YWDOFr2ndZA+TP0PSL4Ikfx8pDi8q9NJARvxjoIuQyn1sdiTtA7lx9TGQqm8PjxFPPqe34jrcvfmVTfFjjAsc4+L7GBeGMs+YVYI5I0xVMq/wtFMBgErj5Bk1qyUwbgwoJjg1RjCMqqlmSlisZsFKhuNvGFqebyvgz1YD/r/Vjp0fu7UYn0NBwXrGnawq0FKhl8VfnJAscOWpEu6cm9VjZ3FrGNPCAipigwFK4q8ZG1AIFFNGW6EYnHcTz3cTz3drjzg+GM+Nw3MympChxcFMx755Aj3t//QcFcnfZdw8fAMCM5H/4gYAAA=="
            }
        }
        response = send_notification_alert(event, {})
        result = json.loads(response['body'])
        self.assertEqual(result, {'data': {'status': 'successful'}, 'error': '', 'status': 'success'})

    @mock.patch('application.handlers.alert_handlers.pause_notification', 'yes')
    def test_pause_notification_alert(self):
        event = {
            "awslogs": {
                "data": "H4sIAAAAAAAAAMXUW2vbMBQH8K8izB7jRZejW2APYUvLYJeH5GlNMIolJ6KObWylXSn97jtO1+0prGzd9mKMJI74/3yO77NDGAa3C6u7LmSz7N18NS8+LpbL+eUim2TtbRN6XDZacs6sNkooXK7b3WXfHjvcmbrbYVq7w9a7qWtcfZdiOeRd3/p8F1LetX2q2jq2+XUXcx+Si/XwWGGZ+uAOWIJTzqcUptxOr159mK8Wy9XGKMVtpUFa76BSpeXgDYjAlJVAyy2WGI7boexjl2LbXMQ6hX7IZldZCkPKNqcbFjehSePifRY9XiSU4YKD4QYMs4JqhQtcgAVQlgpmpWZCUcaYVMAZ49RKyrXEy1JEp+QOGJkpyfh4hGohJ09+WP7q/aeLz5t1GvPkFHJuV1TOJJ8Bfa0FfFmnqqzASCpzIajKAXSVuxBkvrWeBydYJUq5Tm/RJQVPHGnCLemDH/axSqRsmyaUY1pStT3BaKHv+jgEEj3ZOh1cyb0F7SAwvcVIQCFwp7iqzJa4xpPSlXusGxtCHr/YWDOFr2ndZA+TP0PSL4Ikfx8pDi8q9NJARvxjoIuQyn1sdiTtA7lx9TGQqm8PjxFPPqe34jrcvfmVTfFjjAsc4+L7GBeGMs+YVYI5I0xVMq/wtFMBgErj5Bk1qyUwbgwoJjg1RjCMqqlmSlisZsFKhuNvGFqebyvgz1YD/r/Vjp0fu7UYn0NBwXrGnawq0FKhl8VfnJAscOWpEu6cm9VjZ3FrGNPCAipigwFK4q8ZG1AIFFNGW6EYnHcTz3cTz3drjzg+GM+Nw3MympChxcFMx755Aj3t//QcFcnfZdw8fAMCM5H/4gYAAA=="
            }
        }
        response = send_notification_alert(event, {})
        result = json.loads(response['body'])

        self.assertEqual(result, {"status": "failed", "data": {"status": "Not processing"}, "error": ""})

    @mock.patch('application.service.alert_service.ALERT_CONFIG', {})
    @patch('application.service.alert_service.send_slack_message')
    def test_config_none_alert(self, mock_send_team_message):
        event = {
            "awslogs": {
                "data": "H4sIAAAAAAAAAMXUW2vbMBQH8K8izB7jRZejW2APYUvLYJeH5GlNMIolJ6KObWylXSn97jtO1+0prGzd9mKMJI74/3yO77NDGAa3C6u7LmSz7N18NS8+LpbL+eUim2TtbRN6XDZacs6sNkooXK7b3WXfHjvcmbrbYVq7w9a7qWtcfZdiOeRd3/p8F1LetX2q2jq2+XUXcx+Si/XwWGGZ+uAOWIJTzqcUptxOr159mK8Wy9XGKMVtpUFa76BSpeXgDYjAlJVAyy2WGI7boexjl2LbXMQ6hX7IZldZCkPKNqcbFjehSePifRY9XiSU4YKD4QYMs4JqhQtcgAVQlgpmpWZCUcaYVMAZ49RKyrXEy1JEp+QOGJkpyfh4hGohJ09+WP7q/aeLz5t1GvPkFHJuV1TOJJ8Bfa0FfFmnqqzASCpzIajKAXSVuxBkvrWeBydYJUq5Tm/RJQVPHGnCLemDH/axSqRsmyaUY1pStT3BaKHv+jgEEj3ZOh1cyb0F7SAwvcVIQCFwp7iqzJa4xpPSlXusGxtCHr/YWDOFr2ndZA+TP0PSL4Ikfx8pDi8q9NJARvxjoIuQyn1sdiTtA7lx9TGQqm8PjxFPPqe34jrcvfmVTfFjjAsc4+L7GBeGMs+YVYI5I0xVMq/wtFMBgErj5Bk1qyUwbgwoJjg1RjCMqqlmSlisZsFKhuNvGFqebyvgz1YD/r/Vjp0fu7UYn0NBwXrGnawq0FKhl8VfnJAscOWpEu6cm9VjZ3FrGNPCAipigwFK4q8ZG1AIFFNGW6EYnHcTz3cTz3drjzg+GM+Nw3MympChxcFMx755Aj3t//QcFcnfZdw8fAMCM5H/4gYAAA=="
            }
        }
        response = send_notification_alert(event, {})
        result = json.loads(response['body'])
        self.assertEqual(result, {'data': '', 'error': 'BAD_REQUEST'})

    def tearDown(self):
        pass

import base64
import gzip
import json
import os
from datetime import datetime
from http import HTTPStatus

import requests

from common.logger import get_logger
from config import ALERT_CONFIG
from constant import NotificationAlert
from utils.date import datetime_to_str
from utils.exceptions import BadRequestException

logger = get_logger(__name__)

env = os.environ.get('ENVIRONMENT', "default")


def read_config():
    if env in ALERT_CONFIG:
        env_config = ALERT_CONFIG.get(env)
    else:
        env_config = ALERT_CONFIG.get('default')
    return env_config


def generate_cloudwatch_url(log_group, log_stream):
    region = os.getenv('AWS_REGION', "us-west-2")
    return "https://" + region + ".console.aws.amazon.com/cloudwatch/home?region=" + region + "#logsV2:log-groups/log" \
                                                                                              "-group/" + \
           log_group.replace(
               '/', '$252F') + "/log-events/" + log_stream.replace('$', '$2524').replace('[', '$255B').replace(']',
                                                                                                               '$255D').replace(
        '/', '$252F')


def convert_cw_to_event_format(event):
    cw_data = event[NotificationAlert.AWS_LOGS.value][NotificationAlert.DATA.value]
    compressed_payload = base64.b64decode(cw_data)
    uncompressed_payload = gzip.decompress(compressed_payload)
    return json.loads(uncompressed_payload)


def get_data_from_event(payload):
    logGroup = payload[NotificationAlert.LOG_GROUP.value]
    subscription_filters = payload[NotificationAlert.SUBSCRIPTION_FILTERS.value]
    config = read_config()

    if config is None:
        logger.error(f"Config is empty for env")
        raise BadRequestException()

    for key in config:
        if logGroup.find(key) > -1:
            subscription_name = 'default'
            subscription_configs = config[key]
            for subscription_config in subscription_configs:
                if any(subscription_config in subscription_filter for subscription_filter in subscription_filters):
                    subscription_name = subscription_config
                    break

            send_message(subscription_configs[subscription_name], payload)
    logger.info("Successfully processed the request")
    return {"status": "successful"}


def send_slack_message(data):
    data[NotificationAlert.ERROR_MESSAGE.value] = (data[NotificationAlert.ERROR_MESSAGE.value])[0:2000]
    if not data[NotificationAlert.BUTTON_URL.value]:
        data[NotificationAlert.BUTTON_URL.value] = generate_cloudwatch_url(data[NotificationAlert.LOG_GROUP.value],
                                                                           data[NotificationAlert.LOG_STREAM.value])

    slack_format = get_slack_format(log_group=data[NotificationAlert.LOG_GROUP.value],
                                    log_stream=data[NotificationAlert.LOG_STREAM.value],
                                    error_time=data[NotificationAlert.ERROR_TIME.value],
                                    error_message=data[NotificationAlert.ERROR_MESSAGE.value],
                                    image_url=data[NotificationAlert.IMAGE_URL.value],
                                    button_name=data[NotificationAlert.BUTTON_NAME.value],
                                    button_url=data[NotificationAlert.BUTTON_URL.value])

    response = requests.post(data[NotificationAlert.WEBHOOK_URL.value], json.dumps(slack_format),
                             headers={'Content-Type': 'application/json'})
    if response.status_code != HTTPStatus.OK.value:
        logger.error(f"{response.text} and slack json = {json.dumps(slack_format)}")
        raise "Unable to the post the request to slack"

    logger.info(f"Successfully send slack request for {data}")


def send_message(config, payload):
    data = {}
    log_events = payload[NotificationAlert.LOG_EVENTS.value]
    data[NotificationAlert.ENV.value] = env
    data[NotificationAlert.LOG_GROUP.value] = payload[NotificationAlert.LOG_GROUP.value]
    data[NotificationAlert.LOG_STREAM.value] = payload[NotificationAlert.LOG_STREAM.value]
    data[NotificationAlert.BUTTON_URL.value] = generate_cloudwatch_url(payload[NotificationAlert.LOG_GROUP.value],
                                                                       payload[NotificationAlert.LOG_STREAM.value])

    for event in log_events:

        if NotificationAlert.LAMBDA.value in data[NotificationAlert.LOG_GROUP.value]:
            mytimestamp = datetime.fromtimestamp(event[NotificationAlert.TIMESTAMP.value] / 1000)
            data[NotificationAlert.ERROR_TIME.value] = datetime_to_str(mytimestamp)
            data[NotificationAlert.ERROR_MESSAGE.value] = event[NotificationAlert.MESSAGE.value]
        else:
            data[NotificationAlert.ERROR_TIME.value] = event[NotificationAlert.ERROR_TIME.value].split("]", 1)[0] + ']'
            data[NotificationAlert.ERROR_MESSAGE.value] = event[NotificationAlert.ERROR_MESSAGE.value].split("]", 1)[1]

        for individual_team_config in config[NotificationAlert.SLACK.value]:
            send_slack_message({**data, **individual_team_config})


def get_slack_format(log_group, log_stream, error_time, error_message, image_url, button_name, button_url):
    emoji = ":no_entry:" if env == "mt-v2" else ":warning:"
    return {
        'blocks': [
            {
                'type': 'context',
                'elements': [
                    {
                        'type': 'image',
                        'image_url': 'https://image.freepik.com/free-photo/red-drawing-pin_1156-445.jpg',
                        'alt_text': 'images'
                    },
                    {
                        'type': 'mrkdwn',
                        'text': 'Log Group: *' + log_group + '*\n logStream: *' + log_stream + '*'
                    }
                ]
            },
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '>*Environment:* ' + env + " " + emoji + ' \n>*Error Time:* ' + error_time + '\n>*Error Message:* ' + error_message
                },
                'accessory': {
                    'type': 'image',
                    'image_url': image_url,
                    'alt_text': 'Thumbnail'
                }
            },
            {
                'type': 'actions',
                'block_id': 'actionblock789',
                'elements': [
                    {
                        'type': 'button',
                        'text': {
                            'type': 'plain_text',
                            'text': button_name + " " + env
                        },
                        'style': 'primary',
                        'url': button_url
                    }
                ]
            }
        ]
    }

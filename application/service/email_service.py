from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from urllib.parse import urlparse

import boto3
from botocore.exceptions import ClientError
import requests

from common.logger import get_logger
from config import S3_DOWNLOAD_API

logger = get_logger(__name__)
client = boto3.client('ses')


def check_and_fetch_s3_url(attachment_url: str):
    """
    Intermediate function to download attachment from specific S3 Bucket by pre-signed links API
    Checks attachment url and fetches temporary link to download file from S3 Bucket
    If attachment url is not link on S3 download API it will be returned without changes
    """
    parsed_url = urlparse(attachment_url)
    if not parsed_url.hostname == S3_DOWNLOAD_API["HOST"]:
        return attachment_url
    headers = {"Authorization": S3_DOWNLOAD_API["TOKEN"]}
    response = requests.get(attachment_url, headers=headers)
    body = response.json()
    key, download_url = body["key"], body["downloadURL"]
    logger.info(f"Got a link to download {key} file from S3")
    return download_url


def send_email_with_attachment(recipient: str, subject: str, body_html: str,
                               sender: str, attachment_urls: list) -> None:
    logger.info(f"Receipent={recipient}, subject={subject}, body={body_html},"
                f" sender={sender}, attachment_urls={attachment_urls}")
    attachment_filepaths = list()
    try:
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient

        # Set message body
        body = MIMEText(body_html, "html")
        msg.attach(body)

        for attachment_url in attachment_urls:
            logger.info(f"Downloading the file from url={attachment_url}")
            try:
                attachment_url = check_and_fetch_s3_url(attachment_url)
                parsed_url = urlparse(attachment_url)
                filename = os.path.basename(parsed_url.path)
                response = requests.get(attachment_url)
                filepath = f"/tmp/{filename}"
                open(filepath, "wb").write(response.content)
                attachment_filepaths.append(filepath)
                logger.info(f"Download completed for the file from url={attachment_url}")
            except Exception as e:
                logger.exception(f"Unable to download the file from the url={attachment_url} and error={e}")

        logger.info(f"Attachment file path={attachment_filepaths}")
        for attachment_filepath in attachment_filepaths:
            with open(attachment_filepath, "rb") as attachment:
                filename = os.path.basename(attachment_filepath)
                part = MIMEApplication(attachment.read())
                part.add_header("Content-Disposition",
                                "attachment",
                                filename=filename)
            msg.attach(part)

        # Convert message to string and send
        response = client.send_raw_email(
            Source=sender,
            Destinations=list(recipient.split(",")),
            RawMessage={"Data": msg.as_string()}
        )
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
    else:
        logger.info("Email sent! Message ID:"),
        logger.info(response['MessageId'])

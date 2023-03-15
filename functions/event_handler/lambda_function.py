import logging
from os import environ
import sys

import boto3

LOG_LEVEL = environ.get("LOG_LEVEL", "INFO")

logging.basicConfig(
    stream=sys.stdout,
    level=LOG_LEVEL
)
logger = logging.getLogger()

TOPIC_ARN = ''


sns_client = boto3.client('sns')


def event_handler(event, context):
    logger.debug(event)

    # parse event
    pipeline = event.get("detail", {}).get("pipeline", "")
    stage = event.get("detail", {}).get("stage", "")
    state = event.get("detail", {}).get("state", "")

    message = f"Pipeline: {pipeline}\nStage: {stage}\nState: {state}"

    # send SNS message
    response = sns_client.publish(
        TopicArn=TOPIC_ARN,
        Message=message,
        MessageAttributes={
            "stage": {
                "DataType": "string", # https://docs.aws.amazon.com/sns/latest/dg/sns-message-attributes.html#SNSMessageAttributes.DataTypes
                "StringValue": stage
            },
            "pipeline": {
                "DataType": "string",
                "StringValue": pipeline
            }
        }
    )

import logging
from os import environ
import sys

import boto3

LOG_LEVEL = environ.get("LOG_LEVEL", "INFO")

logging.basicConfig(
    stream=sys.stdout,
)
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)

TOPIC_ARN = environ.get("TOPIC_ARN")


sns_client = boto3.client('sns')


def event_handler(event, context):
    logger.debug(event)

    # parse event
    pipeline = event.get("detail", {}).get("pipeline", "")
    stage = event.get("detail", {}).get("stage", "")
    state = event.get("detail", {}).get("state", "")

    message = f"Pipeline: {pipeline}\nStage: {stage}\nState: {state}"

    logger.info(message)

    # send SNS message
    response = sns_client.publish(
        TopicArn=TOPIC_ARN,
        Subject=f"Pipeline Alert: {pipeline}-{stage}-{state}",
        Message=message,
        MessageAttributes={
            "stage": {
                "DataType": "String", # https://docs.aws.amazon.com/sns/latest/dg/sns-message-attributes.html#SNSMessageAttributes.DataTypes
                "StringValue": stage
            },
            "pipeline": {
                "DataType": "String",
                "StringValue": pipeline
            },
            "state": {
                "DataType": "String",
                "StringValue": state
            }
        }
    )

    logger.debug(response)

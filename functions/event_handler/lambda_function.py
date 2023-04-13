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


codepipeline_client = boto3.client('codepipeline')
sns_client = boto3.client('sns')


def event_handler(event, context):
    logger.debug(event)

    # parse event
    event_detail = event.get("detail", {})

    pipeline = event_detail.get("pipeline", "")
    stage = event_detail.get("stage", "")
    state = event_detail.get("state", "")

    # get commit info:
    execution = codepipeline_client.get_pipeline_execution(
        pipelineName=pipeline,
        pipelineExecutionId=event_detail.get("execution-id")
    )

    artifact_revisions = execution.get("pipelineExecution", {}).get("artifactRevisions", [])

    revision_messages = [
        f"    Name: {revision['name']}\n    Id: {revision['revisionId']}\n    Summary: {revision['revisionSummary']}"
        for revision in artifact_revisions
    ]

    revision_join = '\n\n'
    message = f"Pipeline: {pipeline}\nStage: {stage}\nState: {state}\nRevisions:\n{revision_join.join(revision_messages)}"

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

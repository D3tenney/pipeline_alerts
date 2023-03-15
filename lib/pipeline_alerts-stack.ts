import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class PipelineAlertsStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // sns topic
    const topic = new cdk.aws_sns.Topic(this, "Topic", {});

    // lambda?

    const func = new cdk.aws_lambda.Function(this, "HandlerFunc", {
      runtime: cdk.aws_lambda.Runtime.PYTHON_3_9,
      architecture: cdk.aws_lambda.Architecture.ARM_64,
      code: cdk.aws_lambda.Code.fromAsset('./functions/event_handler/'),
      handler: 'lambda_function.event_handler',
      environment: {
        LOG_LEVEL: "DEBUG",
        TOPIC_ARN: topic.topicArn
      }
    });
    topic.grantPublish(func);

    // eventbridge rule

    const pipelineRule = new cdk.aws_events.Rule(this, "PipelineRule", {
      ruleName: 'VoterFileProcessingTriggerRule',
      description: 'Rule that triggers VF step function',
      enabled: true,
      eventPattern: {
        source: [ "aws.codepipeline" ],
        detailType: [ "CodePipeline Stage Execution State Change" ],
        detail: {
          "state": [ "SUCCEEDED", "FAILED", "CANCELED" ]
        },
      },
      targets: [
        //new cdk.aws_events_targets.SnsTopic(topic),
        new cdk.aws_events_targets.LambdaFunction(func)
      ]
    });
  }
}

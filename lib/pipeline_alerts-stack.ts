import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class PipelineAlertsStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // sns topic
    const topic = new cdk.aws_sns.Topic(this, "Topic", {});

    // lambda?

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
        new cdk.aws_events_targets.SnsTopic(topic),
      ]
    });
  }
}

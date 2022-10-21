from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_events as _events,
    aws_events_targets as _events_targets, Duration,
)
from constructs import Construct


class CdkDemoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_layer = _lambda.LayerVersion(
            self,
            id="cdk-demo-layer",
            # python3 -m pip install -r requirements.txt -t modules/python
            code=_lambda.Code.from_asset("modules"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9],
        )

        lambda_function = _lambda.Function(
            self, "CdkDemoLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("functions"),
            handler="lambda_function.handler",
            timeout=Duration.seconds(50),
            layers=[lambda_layer],
        )

        event_rule = _events.Rule(
            self, "CdkDemoEventRule",
            rule_name="cdk-demo-event-rule",
            # schedule=_events.Schedule.cron(minute="*", hour="*"),
            schedule=_events.Schedule.rate(duration=Duration.minutes(1)),
        )

        event_rule.add_target(_events_targets.LambdaFunction(lambda_function))

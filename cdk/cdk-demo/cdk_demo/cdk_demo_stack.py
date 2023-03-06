import typing

from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_events as _events,
    aws_events_targets as _events_targets, Duration,
    # aws_ec2 as _ec2,
    aws_iam as _iam,
)
from constructs import Construct


class CdkDemoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # vpc = _ec2.Vpc(
        #     self,
        #     id="cdk-demo-vpc-id",
        #     cidr="10.0.0.0/16",
        #     nat_gateways=1,
        #     max_azs=2,
        #     subnet_configuration=[
        #         _ec2.SubnetConfiguration(
        #             name="private-subnet-1",
        #             subnet_type=_ec2.SubnetType.PRIVATE_WITH_EGRESS,
        #             cidr_mask=24,
        #         ),
        #         _ec2.SubnetConfiguration(
        #             name="public-subnet-1",
        #             subnet_type=_ec2.SubnetType.PUBLIC,
        #             cidr_mask=24,
        #         ),
        #     ],
        #     # enable_dns_support=True,
        #     # enable_dns_hostnames=True,
        # )

        lambda_role = _iam.Role(
            self,
            id='lambda_role',
            role_name="mail_lambda_role",
            assumed_by=_iam.ServicePrincipal('lambda.amazonaws.com'),
        )

        _iam.ManagedPolicy(
            self,
            id="managed_policy",
            statements=[
                _iam.PolicyStatement(
                    effect=_iam.Effect.ALLOW,
                    actions=[
                        # "ec2:CreateNetworkInterface",
                        # "ec2:DescribeNetworkInterfaces",
                        # "ec2:DeleteNetworkInterface",
                        # "ec2:AssignPrivateIpAddresses",
                        # "ec2:UnassignPrivateIpAddresses",
                        "ses:SendEmail",
                        "ses:SendRawEmail",
                    ],
                    resources=["*"]
                ),
            ],
            roles=[lambda_role],
        )

        lambda_layer = _lambda.LayerVersion(
            self,
            id="cdk-demo-layer",
            # python3 -m pip install -r requirements.txt -t modules/python
            code=_lambda.Code.from_asset("modules"),
            compatible_runtimes=[
                typing.cast(_lambda.Runtime, _lambda.Runtime.PYTHON_3_9),
            ],
        )

        lambda_function = _lambda.Function(
            self,
            current_version_options=_lambda.VersionOptions(),
            id="CdkDemoLambdaFunction",
            runtime=typing.cast(_lambda.Runtime, _lambda.Runtime.PYTHON_3_9),
            code=_lambda.Code.from_asset(path="functions"),
            handler="lambda_function.handler",
            timeout=Duration.seconds(50),
            layers=[
                lambda_layer,
            ],
            architecture=_lambda.Architecture.X86_64,
            # vpc=vpc,
            role=lambda_role,
        )

        _lambda.Alias(
            self,
            id="CdkDemoLambdaAlias",
            alias_name="cdk-demo-lambda-alias",
            version=lambda_function.current_version,
        )

        event_rule = _events.Rule(
            self, "CdkDemoEventRule",
            rule_name="cdk-demo-event-rule",
            # schedule=_events.Schedule.cron(minute="*", hour="*"),
            schedule=_events.Schedule.rate(duration=Duration.minutes(1)),
        )

        event_rule.add_target(_events_targets.LambdaFunction(lambda_function))

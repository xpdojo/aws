# Cloud Development Kit

- [Cloud Development Kit](#cloud-development-kit)
  - [Prerequisites](#prerequisites)
  - [AWS CDK Toolkit](#aws-cdk-toolkit)
    - [Bootstrapping](#bootstrapping)
  - [create cdk app](#create-cdk-app)
    - [Python 3](#python-3)
  - [Lambda with CDK](#lambda-with-cdk)
  - [Diff](#diff)
  - [Synthesizes](#synthesizes)
  - [Deploy](#deploy)

## Prerequisites

- [Install AWS CLI and configure it with credentials.](../aws-cli/README.md)

## AWS CDK Toolkit

- [Install AWS CDK Toolkit (`cdk` command)](https://docs.aws.amazon.com/cdk/v2/guide/cli.html)

AWS CDK CLI를 설치하려면 먼저 Node Package Manager(NPM)가 설치되어 있어야 한다.
다음 명령을 실행하여 AWS CDK CLI를 전역에서 설치한다.

```sh
sudo npm install -g aws-cdk
```

```sh
cdk --version
# 2.46.0 (build 5a0595e)
```

### Bootstrapping

- [Set Up CDK](https://aws.amazon.com/ko/getting-started/guides/setup-cdk/)
- [cdk bootstrap Command](https://docs.aws.amazon.com/cdk/latest/guide/bootstrapping.html)

배포하게 될 대개의 AWS CDK 스택들은 스택과 함께 배포되는
외부 파일(예: AWS Lambda 함수나 Docker 이미지) 등의 자산을 포함하고 있다.
CDK는 이를 Amazon S3 버킷 또는 기타 컨테이너에 업로드하여 배포 중에 AWS CloudFormation에서 사용할 수 있게 한다.
배포하려면 이러한 컨테이너가 AWS 계정 및 배포하려는 리전에 이미 존재해야 한다.
이러한 컨테이너를 생성하는 작업을 부트스트래핑이라고 한다.
AWS 계정(및 해당 리전)을 부트스트랩하려면 다음을 실행한다.

```sh
# Get the account ID
aws sts get-caller-identity
```

```sh
# Bootstrap the account
# cdk bootstrap aws://ACCOUNT-NUMBER/REGION
cdk bootstrap aws://123456789012/ap-northeast-2

# Output
 ⏳  Bootstrapping environment aws://123456789012/ap-northeast-2...
CDKToolkit: creating CloudFormation changeset...
 ✅  Environment aws://123456789012/ap-northeast-2 bootstrapped.
```

다양한 계정과 리전을 사용하려면 각각을 부트스트랩해야 한다.

## create cdk app

```sh
# need a empty directory
mkdir cdk-demo && cd $_
cdk init app --language python
```

### Python 3

- [Working with the AWS CDK in Python](https://docs.aws.amazon.com/cdk/v2/guide/work-with-cdk-python.html) - AWS Developer Guide
- [Python으로 AWS Cloud Development Kit 시작하기](https://aws.amazon.com/ko/blogs/korea/getting-started-with-the-aws-cloud-development-kit-and-python/) - Amazon Web Services 블로그

```sh
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade virtualenv
```

```sh
python3 -m pip install -r requirements.txt
```

```sh
python3 -m pytest -v
```

## Lambda with CDK

```sh
mkdir lambda
touch lambda/lambda_function.py
```

```sh
tree -d -L 1
├── cdk_demo
├── lambda
└── tests
```

```python
# cdk_demo/cdk_demo_stack.py
from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
)
from constructs import Construct


class CdkDemoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        _lambda.Function(
            self,
            "CdkDemoLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("lambda"),
            handler="lambda_function.handler",
        )
```

## Diff

```sh
cdk diff
```

```sh
Stack CdkDemoStack
┌───┬──────────────────────────────────────────┬────────┬────────────────┬──────────────────────────────┬───────────┐
│   │ Resource                                 │ Effect │ Action         │ Principal                    │ Condition │
├───┼──────────────────────────────────────────┼────────┼────────────────┼──────────────────────────────┼───────────┤
│ + │ ${CdkDemoLambdaFunction/ServiceRole.Arn} │ Allow  │ sts:AssumeRole │ Service:lambda.amazonaws.com │           │
└───┴──────────────────────────────────────────┴────────┴────────────────┴──────────────────────────────┴───────────┘
IAM Policy Changes
┌───┬──────────────────────────────────────┬────────────────────────────────────────────────────────────────────────────────┐
│   │ Resource                             │ Managed Policy ARN                                                             │
├───┼──────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────┤
│ + │ ${CdkDemoLambdaFunction/ServiceRole} │ arn:${AWS::Partition}:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole │
└───┴──────────────────────────────────────┴────────────────────────────────────────────────────────────────────────────────┘
(NOTE: There may be security-related changes not in this list. See https://github.com/aws/aws-cdk/issues/1299)

Parameters
[+] Parameter BootstrapVersion BootstrapVersion: {"Type":"AWS::SSM::Parameter::Value<String>","Default":"/cdk-bootstrap/hnb659fds/version","Description":"Version of the CDK Bootstrap resources in this environment, automatically retrieved from SSM Parameter Store. [cdk:skip]"}

Conditions
[+] Condition CDKMetadata/Condition CDKMetadataAvailable: {"Fn::Or":[{"Fn::Or":[{"Fn::Equals":[{"Ref":"AWS::Region"},"af-south-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"ap-east-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"ap-northeast-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"ap-northeast-2"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"ap-south-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"ap-southeast-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"ap-southeast-2"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"ca-central-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"cn-north-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"cn-northwest-1"]}]},{"Fn::Or":[{"Fn::Equals":[{"Ref":"AWS::Region"},"eu-central-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"eu-north-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"eu-south-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"eu-west-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"eu-west-2"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"eu-west-3"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"me-south-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"sa-east-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"us-east-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"us-east-2"]}]},{"Fn::Or":[{"Fn::Equals":[{"Ref":"AWS::Region"},"us-west-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"us-west-2"]}]}]}

Resources
[+] AWS::IAM::Role CdkDemoLambdaFunction/ServiceRole CdkDemoLambdaFunctionServiceRole43ACA25F 
[+] AWS::Lambda::Function CdkDemoLambdaFunction CdkDemoLambdaFunctionBB73AF9F 

Other Changes
[+] Unknown Rules: {"CheckBootstrapVersion":{"Assertions":[{"Assert":{"Fn::Not":[{"Fn::Contains":[["1","2","3","4","5"],{"Ref":"BootstrapVersion"}]}]},"AssertDescription":"CDK bootstrap stack version 6 required. Please run 'cdk bootstrap' with a recent version of the CDK CLI."}]}}
```

## Synthesizes

- 의미
  - ...을 종합[통합]하다; ...을 종합적으로 다루다.
  - [화학] [구성 성분을] 합성하다; ...을 (합성해서) 만들다.
- 기능
  - CDK 앱에서 정의하는 구문에 대한 AWS CloudFormation 템플릿을 생성해서 터미널에 출력한다.

```sh
cdk synth
```

## Deploy

```sh
cdk deploy
```

```sh
<aws_cdk.aws_events.Rule object at 0x7fa5fcc2a110>

✨  Synthesis time: 4.16s

CdkDemoStack: building assets...

CdkDemoStack: assets built

IAM Statement Changes
┌───┬───────────────────────────────┬────────┬───────────────────────────────┬───────────────────────────────┬──────────────────────────────────┐
│   │ Resource                      │ Effect │ Action                        │ Principal                     │ Condition                        │
├───┼───────────────────────────────┼────────┼───────────────────────────────┼───────────────────────────────┼──────────────────────────────────┤
│ + │ ${CdkDemoLambdaFunction.Arn}  │ Allow  │ lambda:InvokeFunction         │ Service:events.amazonaws.com  │ "ArnLike": {                     │
│   │                               │        │                               │                               │   "AWS:SourceArn": "${CdkDemoEve │
│   │                               │        │                               │                               │ ntRule.Arn}"                     │
│   │                               │        │                               │                               │ }                                │
├───┼───────────────────────────────┼────────┼───────────────────────────────┼───────────────────────────────┼──────────────────────────────────┤
│ + │ ${CdkDemoLambdaFunction/Servi │ Allow  │ sts:AssumeRole                │ Service:lambda.amazonaws.com  │                                  │
│   │ ceRole.Arn}                   │        │                               │                               │                                  │
└───┴───────────────────────────────┴────────┴───────────────────────────────┴───────────────────────────────┴──────────────────────────────────┘
IAM Policy Changes
┌───┬──────────────────────────────────────┬────────────────────────────────────────────────────────────────────────────────┐
│   │ Resource                             │ Managed Policy ARN                                                             │
├───┼──────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────┤
│ + │ ${CdkDemoLambdaFunction/ServiceRole} │ arn:${AWS::Partition}:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole │
└───┴──────────────────────────────────────┴────────────────────────────────────────────────────────────────────────────────┘
(NOTE: There may be security-related changes not in this list. See https://github.com/aws/aws-cdk/issues/1299)

Do you wish to deploy these changes (y/n)? y
```

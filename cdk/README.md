# Cloud Development Kit

- [Cloud Development Kit](#cloud-development-kit)
  - [Prerequisites](#prerequisites)
  - [AWS CDK Toolkit](#aws-cdk-toolkit)
    - [Bootstrapping](#bootstrapping)
  - [create cdk app](#create-cdk-app)
    - [Python 3](#python-3)
  - [Lambda with CDK](#lambda-with-cdk)
  - [Diff](#diff)
  - [AWS CloudFormation 템플릿 생성](#aws-cloudformation-템플릿-생성)
  - [AWS CloudFormation 템플릿 배포](#aws-cloudformation-템플릿-배포)
  - [리소스 정리](#리소스-정리)

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

기존에 배포된 스택과 현재 스택의 차이점을 확인한다.

```sh
cdk diff
```

```sh
Stack CdkDemoStack

Resources
[~] AWS::Lambda::Function CdkDemoLambdaFunction CdkDemoLambdaFunctionBB73AF9F 
 ├─ [~] Code
 │   └─ [~] .S3Key:
 │       ├─ [-] f0520ac3db79d59f99f5775cc2a3e9d86613fc281757da6e1c85ae50e12e967e.zip
 │       └─ [+] 589d074650b92e5f2a10a3ccf52aadf3ad03a3b8c5aac0b9f1c02b2c9a2173c5.zip
 └─ [~] Metadata
     └─ [~] .aws:asset:path:
         ├─ [-] asset.f0520ac3db79d59f99f5775cc2a3e9d86613fc281757da6e1c85ae50e12e967e
         └─ [+] asset.589d074650b92e5f2a10a3ccf52aadf3ad03a3b8c5aac0b9f1c02b2c9a2173c5
```

## AWS CloudFormation 템플릿 생성

- 기능
  - CDK 스택을 CloudFormation 스택으로 변환해서 출력한다.
- Synthesizes 의미
  - ...을 종합[통합]하다; ...을 종합적으로 다루다.
  - [화학] [구성 성분을] 합성하다; ...을 (합성해서) 만들다.

```sh
cdk synth
```

## AWS CloudFormation 템플릿 배포

```sh
cdk deploy
```

```sh
<aws_cdk.aws_events.Rule object at 0x7ffaf5ca2c20>

✨  Synthesis time: 4.35s

CdkDemoStack: building assets...

CdkDemoStack: assets built

CdkDemoStack: deploying...

CdkDemoStack: creating CloudFormation changeset...

 ✅  CdkDemoStack

✨  Deployment time: 27.01s

Stack ARN:
arn:aws:cloudformation:ap-northeast-2:123456789012:stack/CdkDemoStack/40e949b0-505b-11ed-8ccf-06e69a4e24e8

✨  Total time: 31.36s
```

## 리소스 정리

```sh
cdk destroy
```

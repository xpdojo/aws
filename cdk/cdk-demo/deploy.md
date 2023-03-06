# Deploying the lambda

## Prerequisites

- [ ] [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) installed
  - [ ] [AWS CLI configured](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html)
- [ ] [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html) installed

## Development

Install the dependencies

```shell
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

이메일 전송을 위해 SES 계정 생성이 필요하다.

> SES > Configuration > Verified identities > Create identity > Email address

이메일 계정을 입력한 후 잠시 기다리면 인증된다.
인증되었으면 IAM에서 해당 리소스에 대한 권한을 부여해야 한다.

> IAM > Users > Permissions > Attah policy > `AmazonSESFullAccess`

## Test

```shell
python -m pytest --log-cli-level=DEBUG
```

## Manage the lambda

- clone the repo
- see the CloudFormation template

```shell
cdk synth
```

- to deploy the lambda

```shell
cdk deploy

✨  Deployment time: 147.64s

Stack ARN:
arn:aws:cloudformation:ap-northeast-2:<id>:stack/CdkDemoStack2/12255440-bbe3-11ed-95bd-0aea68da2362

✨  Total time: 152.58s
```

- to destroy the lambda

```shell
cdk destroy
```

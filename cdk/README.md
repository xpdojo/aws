# Cloud Development Kit

## Prerequisites

- [Install AWS CLI and configure it with credentials.](../aws-cli/README.md)

## AWS CDK Toolkit

- [Install AWS CDK Toolkit (`cdk` command)](https://docs.aws.amazon.com/cdk/v2/guide/cli.html)

```sh
sudo npm install -g aws-cdk
```

```sh
cdk --version
# 2.46.0 (build 5a0595e)
```

## create cdk app

```sh
# need a empty directory
mkdir cdk-sample-app && cd $_
cdk init app --language python
```

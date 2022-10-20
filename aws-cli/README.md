# AWS Command Line Interface

- [AWS Command Line Interface](#aws-command-line-interface)
  - [Install](#install)
  - [Configure](#configure)

## Install

```sh
cd /tmp
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

```sh
aws --version
# aws-cli/2.7.35 Python/3.9.11 Linux/5.15.0-46-generic exe/x86_64.ubuntu.20 prompt/off
```

```sh
aws help
```

## Configure

`aws` 명령어를 사용하려면 구성(configure)이 필요하다.

- IAM > Secrutiy Credentials (보안 자격 증명)
  - Access keys (access key ID and secret access key)
  - Create a new access key

```sh
sh> aws configure
AWS Access Key ID [None]: ${ACCESS_KEY_ID}
AWS Secret Access Key [None]: ${SECRET_ACCESS_KEY}
Default region name [None]: ap-northeast-2 # Seoul
Default output format [None]: json # json, text, table
```

```sh
sh> cat ~/.aws/config
[default]
region = ap-northeast-2
output = json
```

```sh
sh> cat ~/.aws/credentials
[default]
aws_access_key_id = ${ACCESS_KEY_ID}
aws_secret_access_key = ${SECRET_ACCESS_KEY}
```

구성이 끝났으면 STS(Security Token Service)로 identity를 확인해본다.

```sh
# IAM 사용자라면 조금 다르게 표시된다.
sh> aws sts get-caller-identity
{
  "UserId": "123456789012", # 12-digit number
  "Account": "123456789012", # 12-digit number
  "Arn": "arn:aws:iam::123456789012:root"
}
```

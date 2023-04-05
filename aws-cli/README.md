# AWS Command Line Interface

- [AWS Command Line Interface](#aws-command-line-interface)
  - [명령줄 도구 설치](#명령줄-도구-설치)
    - [설치 확인](#설치-확인)
  - [Configure](#configure)
    - [프로파일(Profile) 나누기](#프로파일profile-나누기)
    - [default 변경하기](#default-변경하기)

## 명령줄 도구 설치

```sh
cd /tmp
```

```sh
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
```

```sh
unzip awscliv2.zip
```

```sh
sudo ./aws/install
```

### 설치 확인

```sh
aws --version
# aws-cli/2.7.35 Python/3.9.11 Linux/5.15.0-46-generic exe/x86_64.ubuntu.20 prompt/off
```

```sh
aws help
```

## Configure

`aws` 명령어를 사용하려면 구성(configure)이 필요하다.

- [IAM > My secrutiy Credentials (보안 자격 증명)](https://us-east-1.console.aws.amazon.com/iamv2/home#/security_credentials)
  - Access keys (access key ID and secret access key)
    - Create a new access key
      - [Command Line Interface(CLI)](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)

```sh
aws configure
```

```sh
AWS Access Key ID [None]: ${ACCESS_KEY_ID}
AWS Secret Access Key [None]: ${SECRET_ACCESS_KEY}
Default region name [None]: ap-northeast-2 # Seoul
Default output format [None]: json # json, text, table
```

구성 파일은 `$HOME/.aws`에 저장된다.

```sh
# ~/.aws/config
[default]
region = ap-northeast-2
output = json

# ~/.aws/credentials
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

```sh
aws configure list
```

```sh
      Name                    Value             Type    Location
      ----                    -----             ----    --------
   profile                <not set>             None    None
access_key     ****************NGXR shared-credentials-file
secret_key     ****************o7/A shared-credentials-file
    region           ap-northeast-2      config-file    ~/.aws/config
```

### 프로파일(Profile) 나누기

아무 옵션없이 설정하면 기본적으로 `default` 프로파일을 사용하고 있다.
하지만 개인 계정, IAM, Root 등 여러 계정을 사용하고 있다면 프로파일을 나누어 사용하는 것이 좋다.

```sh
aws configure --profile personal
```

```sh
AWS Access Key ID [None]: ${ACCESS_KEY_ID}
AWS Secret Access Key [None]: ${SECRET_ACCESS_KEY}
Default region name [None]: ap-northeast-2 # Seoul
Default output format [None]: json # json, text, table
```

프로파일이 추가되었는지 확인한다.

```sh
aws configure list-profiles                                                                                                ✭
# default
# personal
```

```sh
aws configure list --profile personal
```

```sh
# default와 달리 profile이 표시된다.
      Name                    Value             Type    Location
      ----                    -----             ----    --------
   profile                 personal           manual    --profile
access_key     ****************2RER shared-credentials-file    
secret_key     ****************nmQR shared-credentials-file    
    region           ap-northeast-2      config-file    ~/.aws/config
```

이후 명령어를 사용할 때는 `--profile` 옵션을 사용한다.

```sh
aws s3 ls --profile personal
```

[테라폼](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)에서도
`profile`을 사용할 수 있다.

```hcl
provider "aws" {
  region = "ap-northeast-2"
  profile = "personal"
}
```

### default 변경하기

TODO

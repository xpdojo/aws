# EC2

- [EC2](#ec2)
  - [help](#help)
  - [키 페어(Key pair) 관리](#키-페어key-pair-관리)
    - [키 페어 생성](#키-페어-생성)
    - [키 페어 조회](#키-페어-조회)
    - [public key만 추출](#public-key만-추출)
    - [로컬에 있는 키를 등록](#로컬에-있는-키를-등록)
    - [키 페어 제거](#키-페어-제거)
  - [인스턴스 생성](#인스턴스-생성)
  - [인스턴스 조회](#인스턴스-조회)
  - [대상 그룹(Target Group) 생성](#대상-그룹target-group-생성)
  - [Target Group 조회](#target-group-조회)
  - [인스턴스 이름을 기준으로 리스팅](#인스턴스-이름을-기준으로-리스팅)
  - [Instance Profile은 생성 후 할당해도 됨](#instance-profile은-생성-후-할당해도-됨)
  - [인스턴스 생성 후 태그 추가](#인스턴스-생성-후-태그-추가)
  - [인스턴스 일시 중지](#인스턴스-일시-중지)
  - [일시 중지한 인스턴스 재시작](#일시-중지한-인스턴스-재시작)
  - [인스턴스 종료](#인스턴스-종료)
  - [인스턴스에 고정 IP(EIP, Elastic IP) 할당하기](#인스턴스에-고정-ipeip-elastic-ip-할당하기)
  - [참조](#참조)

## help

```sh
aws ec2 help
```

## 키 페어(Key pair) 관리

### 키 페어 생성

- [Create a key pair using Amazon EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/create-key-pairs.html#having-ec2-create-your-key-pair)

```sh
aws ec2 create-key-pair \
  --key-name my-key-pair \
  --key-type ed25519 \
  --query "KeyMaterial" \
  --key-format pem \
  --output text > my-key-pair.pem
```

### 키 페어 조회

```sh
# 전체 키 페어 조회
aws ec2 describe-key-pairs
```

```sh
# 특정 키 페어 조회
aws ec2 describe-key-pairs --key-name my-key-pair --include-public-key
```

```json
// response
{
    "KeyPairs": [
        {
            "KeyPairId": "key-071666eea9eb3d80b",
            "KeyFingerprint": "8bEKkG1XmUyLfpioZADSL3xw7R7YchKUc1velSSLJmI=",
            "KeyName": "my-key-pair",
            "KeyType": "ed25519",
            "Tags": [],
            "PublicKey": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKaZ7+euMqXcICxcOuGSdwqJcqIrZxbpt4qVrnS1F91m my-key-pair",
            "CreateTime": "2023-06-22T08:54:03.314000+00:00"
        }
    ]
}
```

### public key만 추출

```sh
aws ec2 describe-key-pairs \
  --key-name my-key-pair \
  --include-public-key \
  --query "KeyPairs[*].PublicKey" \
  --output text > my-key-pair.pub
```

### 로컬에 있는 키를 등록

```sh
aws ec2 import-key-pair \
  --key-name "my-key-pair" \
  --public-key-material fileb://./my-key-pair.pub
```

### 키 페어 제거

```sh
aws ec2 delete-key-pair --key-name my-key-pair
```

## 인스턴스 생성

- 앞서 생성한 키 페어 할당
- 인스턴스 프로파일은 나중에 할당해도 됨
- `ami-0c9c942bd7bf113a2`는 Ubuntu Server 22.04 LTS (HVM), SSD Volume Type, 64비트 (x86)

```sh
aws ec2 run-instances \
  --image-id ami-0c9c942bd7bf113a2 \
  --count 2 \
  --instance-type t2.micro \
  # 아래는 모두 선택 사항
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=demo-instance},{Key=env,Value=production}]' 'ResourceType=volume,Tags=[{Key=Name,Value=demo-volume}]' \
  --key-name my-key-pair \
  --subnet-id subnet-12345678901234567 \
  --security-group-ids sg-12345678901234567 \
  --iam-instance-profile Name=$INSTANCE_PROFILE_NAME
```

## 인스턴스 조회

```sh
aws ec2 describe-instances
```

## 대상 그룹(Target Group) 생성

```sh
aws elbv2 create-target-group \
  --name demo-target-group \
  --protocol HTTP \
  --port $APPLICATION_PORT \
  --target-type instance \
  --vpc-id vpc-12345678901234567
```

## Target Group 조회

```sh
aws elbv2 describe-target-groups
```

## 인스턴스 이름을 기준으로 리스팅

```sh
aws ec2 describe-instances --filters "Name=tag:Name,Values=*demo*
```

```sh
aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=*demo*" \
  --query "Reservations[*].Instances[*].{Name:Tags[?Key=='Name']|[0].Value,InstanceProfile:IamInstanceProfile.Arn}" \
  --output json
```

```json
[
    [
        {
            "Name": "demo-instance",
            "InstanceProfile": "arn:aws:iam::123456789012:instance-profile/$INSTANCE_PROFILE_NAME"
        }
    ]
]
```

```sh
aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=*demo*" \
  --query "Reservations[*].Instances[*].{Instance:InstanceId,Name:Tags[?Key=='Name']|[0].Value,State:State.Name}" \
  --output table
```

```text
--------------------------------------------------------
|                   DescribeInstances                  |
+---------------------+-----------------+--------------+
|      Instance       |      Name       |    State     |
+---------------------+-----------------+--------------+
|  i-0054ddf98d59192fa|  demo-instance  |  running     |
|  i-095f7191ca957750c|  demo-instance  |  terminated  |
+---------------------+-----------------+--------------+
```

## Instance Profile은 생성 후 할당해도 됨

Instance Profile 생성

```sh
aws iam create-instance-profile --instance-profile-name $INSTANCE_PROFILE_NAME
```

생성한 Instance Profile 조회

```sh
aws iam list-instance-profiles
```

Instance Profile에 Role 할당

```sh
aws iam add-role-to-instance-profile \
  --role-name $CODE_DEPLOY_ROLE_NAME \
  --instance-profile-name $INSTANCE_PROFILE_NAME
```

EC2 인스턴스에 Instance Profile 할당

```sh
aws ec2 associate-iam-instance-profile \
  --instance-id i-1234567890abcdef0 \
  --iam-instance-profile Name=$INSTANCE_PROFILE_NAME
```

## 인스턴스 생성 후 태그 추가

```sh
aws ec2 create-tags \
  --resources i-1234567890abcdef0 \
  --tags Key=Name,Value=MyInstance
```

## 인스턴스 일시 중지

```sh
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
```

## 일시 중지한 인스턴스 재시작

```sh
aws ec2 start-instances --instance-ids i-1234567890abcdef0
```

## 인스턴스 종료

```sh
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0
```

```json
{
    "TerminatingInstances": [
        {
            "CurrentState": {
                "Code": 32,
                "Name": "shutting-down"
            },
            "InstanceId": "i-095f7191ca957750c",
            "PreviousState": {
                "Code": 16,
                "Name": "running"
            }
        }
    ]
}
```

## 인스턴스에 고정 IP(EIP, Elastic IP) 할당하기

- SMS, Email API와 같은 외부 서비스를 사용하려면 IP를 whitelist에 등록해야 한다.
- EC2는 재시작 시 IP가 변동되기 때문에 외부 API를 사용하려면 고정 IP가 필요하다.

먼저 Elastic IP를 생성한다.

```sh
aws ec2 allocate-address \
  --domain vpc \
  --tag-specifications "ResourceType=elastic-ip,Tags=[{Key=Name,Value=my-apiserver-eip},{Key=domain,Value=my-domain}]"
```

```json
// response
{
    "PublicIp": "13.255.255.255",
    "AllocationId": "eipalloc-123449f28ae7ddemo",
    "PublicIpv4Pool": "amazon",
    "NetworkBorderGroup": "ap-northeast-2",
    "Domain": "vpc"
}
```

- 다시 만드려면 기존에 만든 걸 release 하자.

```sh
aws ec2 release-address --allocation-id $AllocationId
```

- 인스턴스 ID를 콘솔 혹은 CLI로 확인한다.

```sh
aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=*my-instance*" \
  --query "Reservations[*].Instances[*].{InstanceId:InstanceId}"
```

```json
[
    [
        {
            "InstanceId": "i-1234b56d7dd26demo"
        }
    ]
]
```

해당 AllocationId를 Instance에 할당한다.

```sh
aws ec2 associate-address --instance-id $InstanceId --allocation-id $AllocationId
```

```sh
{
    "AssociationId": "eipassoc-1234eba63db7edemo"
}
```

## 참조

- [Launching, listing, and terminating Amazon EC2 instances](https://docs.aws.amazon.com/cli/latest/userguide/cli-services-ec2-instances.html)

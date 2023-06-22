# EC2

- [EC2](#ec2)
  - [인스턴스 이름을 기준으로 리스팅](#인스턴스-이름을-기준으로-리스팅)
  - [인스턴스 생성](#인스턴스-생성)
  - [Instance Profile은 생성 후 할당해도 됨](#instance-profile은-생성-후-할당해도-됨)
  - [인스턴스 생성 후 태그 추가](#인스턴스-생성-후-태그-추가)
  - [인스턴스 일시 중지](#인스턴스-일시-중지)
  - [일시 중지한 인스턴스 재시작](#일시-중지한-인스턴스-재시작)
  - [인스턴스 종료](#인스턴스-종료)
  - [인스턴스에 고정 IP(EIP, Elastic IP) 할당하기](#인스턴스에-고정-ipeip-elastic-ip-할당하기)
  - [참조](#참조)

```sh
aws ec2 help
```

## 인스턴스 이름을 기준으로 리스팅

```sh
aws ec2 describe-instances --filters "Name=tag:Name,Values=*markruler*
```

```sh
aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=*markruler*" \
  --query "Reservations[*].Instances[*].{Name:Tags[?Key=='Name']|[0].Value,InstanceProfile:IamInstanceProfile.Arn}" \
  --output json
```

```json
[
    [
        {
            "Name": "markruler-apiserver-dev",
            "InstanceProfile": "arn:aws:iam::123456789012:instance-profile/markruler-instnace-profile"
        }
    ]
]
```

```sh
aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=*markruler*" \
  --query "Reservations[*].Instances[*].{Instance:InstanceId,Name:Tags[?Key=='Name']|[0].Value,State:State.Name}" \
  --output table
```

```text
--------------------------------------------------------------
|                      DescribeInstances                     |
+----------------------+--------------------------+----------+
|       Instance       |          Name            |  State   |
+----------------------+--------------------------+----------+
|  i-0869b56d7dd263ee0 |  winipass-apiserver-dev  |  running |
+----------------------+--------------------------+----------+
```

## 인스턴스 생성

```sh
aws ec2 run-instances \
  --image-id ami-abc12345 \
  --count 1 \
  --instance-type t2.micro \
  --iam-instance-profile Name=$INSTANCE_PROFILE_NAME
```

## Instance Profile은 생성 후 할당해도 됨

- Instance Profile 생성

```sh
aws iam create-instance-profile --instance-profile-name $INSTANCE_PROFILE_NAME
```

- Instance Profile에 Role 할당

```sh
aws iam add-role-to-instance-profile \
  --role-name $CODE_DEPLOY_ROLE_NAME \
  --instance-profile-name $INSTANCE_PROFILE_NAME
```

- EC2 인스턴스에 Instance Profile 할당

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

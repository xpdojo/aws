# CodeDeploy

- [CodeDeploy](#codedeploy)
  - [CodeDeploy 배포 그룹에 할당할 IAM Role 추가](#codedeploy-배포-그룹에-할당할-iam-role-추가)
  - [CodeDeploy 설정](#codedeploy-설정)
  - [EC2 인스턴스에 IAM Role 할당](#ec2-인스턴스에-iam-role-할당)
  - [배포](#배포)
  - [CodeDeploy Agent](#codedeploy-agent)
    - [Issue](#issue)

## CodeDeploy 배포 그룹에 할당할 IAM Role 추가

- [서비스 역할 생성(CLI)](https://docs.aws.amazon.com/ko_kr/codedeploy/latest/userguide/getting-started-create-service-role.html#getting-started-create-service-role-cli)
  - Role을 정의한 JSON 파일을 만든다. (`CodeDeploy-Trust.json`)

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": [
                    "codedeploy.amazonaws.com"
                ]
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

- 해당 JSON 파일을 기반으로 Role을 생성한다.

```sh
aws iam create-role \
  --role-name ${ROLE_NAME} \
  --assume-role-policy-document file://CodeDeploy-Trust.json
```

- 생성한 Role에 `AWSCodeDeployRole` Policy를 추가한다.

```sh
aws iam attach-role-policy \
  --role-name ${ROLE_NAME} \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSCodeDeployRole
```

- 해당 Role의 ARN(Amazon Resource Name)을 확인한다.

```sh
aws iam get-role \
  --role-name ${ROLE_NAME} \
  --query "Role.Arn" --output text
```

```sh
# arn:aws:iam::123456789012:role/${ROLE_NAME}
```

## CodeDeploy 설정

CodeDeploy에 애플리케이션(Application)을 만든다.

```sh
aws deploy create-application --application-name ${APPLICATION_NAME}
```

CodeDeploy에 배포 그룹(Deployment Group)을 만든다.

- 위에서 생성한 Role ARN을 추가한다.
- EC2 Tag Filter는 해당 배포 그룹이 실행되었을 때 배포할 EC2 인스턴스의 태그를 지정한다.
  - 만약 `Type`이 `KEY_AND_VALUE`라면 `Key`와 `Value`가 모두 일치해야 배포된다.

```sh
aws deploy create-deployment-group \
  --deployment-group-name ${DEPLOYMENT_GROUP_NAME} \
  --application-name ${APPLICATION_NAME} \
  --service-role-arn ${ROLE_ARN}
  --ec2-tag-filters Key=Name,Value=${EC2_INSTANCE_NAME},Type=KEY_AND_VALUE
```

- 배포할 프로젝트를 압축 파일(zip) 형태로 담을 S3 버킷을 만든다.
  - 아래 명령어를 사용하면 자동으로 압축해준다.
- 해당 S3 버킷에 프로젝트를 배포한다.
  - `GITHUB_SHA`는 GitHub Action 사용 시 만드는 해시값이기 때문에
    GitHub Action을 사용하지 않을 경우 임의의 값(epoch time 등)을 넣을 수 있다.

```sh
aws deploy push \
  --application-name ${APPLICATION_NAME} \
  --ignore-hidden-files \
  --s3-location s3://${{ vars.BUCKET_NAME }}/${GITHUB_SHA}.zip \
  --source .
```

## EC2 인스턴스에 IAM Role 할당

인스턴스 프로파일을 만든다.

- [Troubleshoot unavailable IAM roles when launching instances](https://repost.aws/knowledge-center/iam-role-not-in-list)

```sh
aws iam create-instance-profile --instance-profile-name $INSTANCE_PROFILE_NAME
```

```json
// response
{
    "InstanceProfile": {
        "Path": "/",
        "InstanceProfileName": "$INSTANCE_PROFILE_NAME",
        "InstanceProfileId": "DEMORLF6AMB6UZULG6U5M",
        "Arn": "arn:aws:iam::123456789012:instance-profile/$INSTANCE_PROFILE_NAME",
        "CreateDate": "2023-06-20T07:14:55+00:00",
        "Roles": []
    }
}
```

EC2에 할당할 Role을 생성한다. (`EC2RoleforCodeDeploy.json`)

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": [
                    "ec2.amazonaws.com"
                ]
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

```sh
aws iam create-role \
  --role-name $EC2_ROLE_NAME \
  --assume-role-policy-document file://EC2RoleforCodeDeploy.json
```

`AmazonEC2RoleforAWSCodeDeploy` 권한을 할당한다.

```sh
aws iam attach-role-policy \
  --role-name $EC2_ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforAWSCodeDeploy
```

인스턴스 프로파일에 Role을 추가한다.

```sh
aws iam add-role-to-instance-profile \
  --role-name $CODE_DEPLOY_ROLE_NAME \
  --instance-profile-name $INSTANCE_PROFILE_NAME
```

인스턴스 프로파일에 추가된 Role을 인스턴스에 할당한다.

```sh
aws ec2 associate-iam-instance-profile \
  --instance-id $INSTANCE_ID \
  --iam-instance-profile Name=$INSTANCE_PROFILE_NAME
```

인스턴스 정보에서 IAM 역할(Role)을 확인할 수 있다.

```sh
aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=*my-ec2*" \
  --query "Reservations[*].Instances[*].{Name:Tags[?Key=='Name']|[0].Value,InstanceProfile:IamInstanceProfile.Arn}" \
  --output json
```

```json
[
    [
        {
            "Name": "my-ec2-instance",
            "InstanceProfile": "arn:aws:iam::12345789012:instance-profile/my-ec2-instance"
        }
    ]
]
```

## 배포

프로젝트에 CodeDeploy의 작업 명세서인 `appspec.yml`을 만든다.

- 스크립트 출처: [Github Action과 AWS CodeDeploy를 사용한 CI/CD 구축 방법](https://chae528.tistory.com/100)

```yaml
version: 0.0
os: linux

files:
  - source:  /
    destination: /home/ubuntu/app
    overwrite: yes

permissions:
  - object: /
    pattern: "**"
    owner: ubuntu
    group: ubuntu

hooks:
  AfterInstall:
    - location: scripts/code-deploy/after-install.sh
      timeout: 60
      runas: ubuntu
  ApplicationStart:
    - location: scripts/code-deploy/application-start.sh
      timeout: 60
      runas: ubuntu
```

```sh
#!/usr/bin/env bash
# after-install.sh

PROJECT_ROOT="/home/ubuntu/app" # appspec.yaml에 적은 files.destination
JAR_FILE="$PROJECT_ROOT/artifact.jar"
JAVA_BIN="/home/ubuntu/jdk/temurin-17.0.6/bin/java"

APP_LOG="$PROJECT_ROOT/application.log"
ERROR_LOG="$PROJECT_ROOT/error.log"
DEPLOY_LOG="$PROJECT_ROOT/deploy.log"

TIME_NOW=$(date +%c)

PROFILE="dev"

echo "$TIME_NOW > [RUN] $JAR_FILE" >>$DEPLOY_LOG
nohup $JAVA_BIN -jar -Dspring.profiles.active=$PROFILE \
  -Xms256m \
  -Xmx256m \
  $JAR_FILE >$APP_LOG 2>$ERROR_LOG &

CURRENT_PID=$(pgrep -f $JAR_FILE)
echo "$TIME_NOW > [RUN] PID=$CURRENT_PID" >>$DEPLOY_LOG
```

```sh
#!/usr/bin/env bash
# application-start.sh

PROJECT_ROOT="/home/ubuntu/app"
JAR_FILE="$PROJECT_ROOT/artifact.jar"

DEPLOY_LOG="$PROJECT_ROOT/deploy.log"

TIME_NOW=$(date +%c)

CURRENT_PID=$(pgrep -f $JAR_FILE)

if [ -z $CURRENT_PID ]; then
  echo "$TIME_NOW > [NOT_FOUND] 현재 실행중인 애플리케이션이 없습니다." >> $DEPLOY_LOG
else
  echo "$TIME_NOW > [KILL] PID=$CURRENT_PID " >> $DEPLOY_LOG
  kill -15 $CURRENT_PID
fi
```

## CodeDeploy Agent

위 `appspec.yml` 작업을 실행할 CodeDeploy Agent를 EC2 인스턴스에 설치 및 실행해야 한다.

- [Resource kit bucket names by Region](https://docs.aws.amazon.com/codedeploy/latest/userguide/resource-kit.html#resource-kit-bucket-names)
  - 버전이나 리전을 확인 후 설치한다.

```sh
sudo apt update
sudo apt install ruby-full wget
```

```sh
wget https://aws-codedeploy-ap-northeast-2.s3.ap-northeast-2.amazonaws.com/latest/install
```

```sh
chmod +x ./install
```

```sh
sudo ./install auto > /tmp/logfile
```

```sh
sudo systemctl status codedeploy-agent
```

CodeDeploy에 배포(Deployment)를 만든다.

- 지정한 배포 그룹으로 필터링된 EC2 인스턴스에 S3에 배포된 프로젝트가 배포된다.
- 그럼 EC2 인스턴스에 실행 중인 CodeDeploy Agent가 appspec.yml에 적힌 작업 명세서를 보고 스크립트를 실행한다.

```sh
aws deploy create-deployment \
  --application-name $APPLICATION_NAME \
  --deployment-config-name CodeDeployDefault.OneAtATime \
  --deployment-group-name $DEPLOYMENT_GROUP_NAME \
  --s3-location bucket=$BUCKET_NAME,bundleType=zip,key=$GITHUB_SHA.zip
```

### Issue

```sh
2023-06-20T08:30:09 ERROR [codedeploy-agent(77037)]: InstanceAgent::Plugins::CodeDeployPlugin::CommandPoller: Missing credentials - please check if this instance was started with an IAM instance profile
```

CodeDeploy Agent를 실행한 상태에서 Role을 부여할 경우, 위와 같은 에러가 발생할 수 있다.
재시작하면 해결된다.

```sh
sudo systemctl restart codedeploy-agent
```

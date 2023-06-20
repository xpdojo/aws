# CodeDeploy

- [참조](https://docs.aws.amazon.com/ko_kr/codedeploy/latest/userguide/getting-started-create-service-role.html#getting-started-create-service-role-cli)

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

```sh
aws iam create-role \
  --role-name $ROLE_NAME \
  --assume-role-policy-document file://CodeDeploy-Trust.json
```

```json
{
    "Role": {
        "Path": "/",
        "RoleName": "$ROLE_NAME",
        "RoleId": "AROARLF6AMB67RSKCRGBD",
        "Arn": "arn:aws:iam::123456789012:role/$ROLE_NAME",
        "CreateDate": "2023-06-20T03:42:04+00:00",
        "AssumeRolePolicyDocument": {
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
    }
}
```

```sh
aws iam attach-role-policy \
  --role-name $ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSCodeDeployRole
```

```sh
aws iam get-role \
  --role-name $ROLE_NAME \
  --query "Role.Arn" --output text
```

```sh
arn:aws:iam::123456789012:role/$ROLE_NAME
```

```sh
aws deploy create-application --application-name $APPLICATION_NAME
```

```sh
aws deploy create-deployment-group \
  --deployment-group-name $DEPLOYMENT_GROUP_NAME \
  --application-name $APPLICATION_NAME \
  --service-role-arn $ROLE_ARN
  --ec2-tag-filters Key=Name,Value=$EC2_INSTANCE_NAME,Type=KEY_AND_VALUE
```

```json
{
    "deploymentGroupId": "641c13a2-5e91-4f65-9b7f-4f77aa162629"
}
```

```sh
aws deploy push \
  --application-name $APPLICATION_NAME \
  --ignore-hidden-files \
  --s3-location s3://${{ vars.BUCKET_NAME }}/$GITHUB_SHA.zip \
  --source .
```

```sh
aws deploy create-deployment \
  --application-name $APPLICATION_NAME \
  --deployment-config-name CodeDeployDefault.OneAtATime \
  --deployment-group-name $DEPLOYMENT_GROUP_NAME \
  --s3-location bucket=${{ vars.BUCKET_NAME }},bundleType=zip,key=$GITHUB_SHA.zip
```

- https://repost.aws/knowledge-center/iam-role-not-in-list

```sh
aws iam create-instance-profile --instance-profile-name $INSTANCE_PROFILE_NAME
```

```json
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

```sh
aws iam add-role-to-instance-profile \
  --role-name $CODE_DEPLOY_ROLE_NAME \
  --instance-profile-name $INSTANCE_PROFILE_NAME
```

## Issue

```sh
2023-06-20T08:30:09 ERROR [codedeploy-agent(77037)]: InstanceAgent::Plugins::CodeDeployPlugin::CommandPoller: Missing credentials - please check if this instance was started with an IAM instance profile
```

CodeDeploy Agent를 실행한 상태에서 Role을 부여할 경우, 위와 같은 에러가 발생할 수 있다.
재시작하면 해결된다.

```sh
sudo systemctl restart codedeploy-agent
```

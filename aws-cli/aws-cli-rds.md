# Amazon RDS

Amazon Relational Database Service (RDS)

```sh
aws configure list-profiles
```

```sh
aws list-commands
```

## RDS 명령어 설명과 하위 명령어 조회

```sh
aws rds help
```

## RDS 인스턴스 목록

- [커맨드라인 JSON 프로세서 jq](https://www.44bits.io/ko/post/cli_json_processor_jq_basic_syntax) - 44Bits

```sh
aws rds describe-db-instances | jq '.[] | .[] | .DBInstanceIdentifier'
# "rds-instance-1"
# "rds-instance-2"
```

## RDS 인스턴스 생성

- 생성 후 자동으로 시작한다.

```sh
# https://docs.aws.amazon.com/cli/latest/reference/rds/create-db-instance.html#examples
# engine-version: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/MySQL.Concepts.VersionMgmt.html
DB_INSTANCE_IDENTIFIER="test-instance-1"
aws rds create-db-instance \
    --db-instance-identifier ${DB_INSTANCE_IDENTIFIER} \
    --db-instance-class db.t3.micro \
    --engine mysql \
    --engine-version 5.7 \
    --master-username admin \
    --master-user-password secret99 \
    --allocated-storage 20
```

## RDS 인스턴스 일시 중지

```sh
aws rds stop-db-instance --db-instance-identifier ${DB_INSTANCE_IDENTIFIER}
```

## RDS 인스턴스 시작

`start-db-instance`는 이미 생성되어 있는 인스턴스 시작하는 것임.

```sh
aws rds start-db-instance --db-instance-identifier ${DB_INSTANCE_IDENTIFIER}
```

```sh
aws rds describe-db-instances | jq '.[] | .[] | select(.DBInstanceIdentifier=="'"${DB_INSTANCE_IDENTIFIER}"'")'
# {
#   "DBInstanceIdentifier": "test-instance-1",
#   "DBInstanceClass": "db.t2.micro",
#   "Engine": "mysql",
#   "DBInstanceStatus": "starting",
#   ...
# }
```

## RDS 인스턴스 제거

```sh
# `--skip-final-snapshot`: RDS doesn't create a DB snapshot.
aws rds delete-db-instance --db-instance-identifier ${DB_INSTANCE_IDENTIFIER} --skip-final-snapshot
```

## 파라미터 그룹 관리

- [Working with DB parameter groups](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithDBInstanceParamGroups.html)

```sh
aws rds create-db-parameter-group \
    --db-parameter-group-name ${PARAMTER_GROUP_NAME} \
    --db-parameter-group-family mysql5.7 \
    --description "My Parameter Group"
```

- 분명 `--parameters`가 `list`라고 되어 있는데 한번에 보내면 변경되지 않는다...

```sh
# Encoding
# https://medium.com/oldbeedev/mysql-utf8mb4-character-set-%EC%84%A4%EC%A0%95%ED%95%98%EA%B8%B0-da7624958624
# https://blog.gangnamunni.com/post/aws-rds-mysql-utf8mb4/
aws rds modify-db-parameter-group \
    --db-parameter-group-name ${PARAMETER_GROUP_NAME} \
    --parameters "ParameterName=skip-character-set-client-handshake, ParameterValue=1, ApplyMethod=pending-reboot"

aws rds modify-db-parameter-group \
    --db-parameter-group-name ${PARAMETER_GROUP_NAME} \
    --parameters "ParameterName=collation_server, ParameterValue=utf8mb4_unicode_ci, ApplyMethod=immediate"

aws rds modify-db-parameter-group \
    --db-parameter-group-name ${PARAMETER_GROUP_NAME} \
    --parameters "ParameterName=character_set_client, ParameterValue=utf8mb4, ApplyMethod=immediate"

aws rds modify-db-parameter-group \
    --db-parameter-group-name ${PARAMETER_GROUP_NAME} \
    --parameters "ParameterName=character_set_server, ParameterValue=utf8mb4, ApplyMethod=immediate"

aws rds modify-db-parameter-group \
    --db-parameter-group-name ${PARAMETER_GROUP_NAME} \
    --parameters "ParameterName=character_set_connection, ParameterValue=utf8mb4, ApplyMethod=immediate"

aws rds modify-db-parameter-group \
    --db-parameter-group-name ${PARAMETER_GROUP_NAME} \
    --parameters "ParameterName=character_set_database, ParameterValue=utf8mb4, ApplyMethod=immediate"

aws rds modify-db-parameter-group \
    --db-parameter-group-name ${PARAMETER_GROUP_NAME} \
    --parameters "ParameterName=character_set_results, ParameterValue=utf8mb4, ApplyMethod=immediate"

aws rds modify-db-parameter-group \
    --db-parameter-group-name ${PARAMETER_GROUP_NAME} \
    --parameters "ParameterName=character_set_filesystem, ParameterValue=binary, ApplyMethod=immediate"

# Time Zone
aws rds modify-db-parameter-group \
    --db-parameter-group-name ${PARAMETER_GROUP_NAME} \
    --parameters "ParameterName=time_zone, ParameterValue=Asia/Seoul, ApplyMethod=immediate"
```

만든 파라미터 그룹을 RDS 인스턴스에 적용한다.

```sh
aws rds modify-db-instance \
    --db-instance-identifier ${DB_INSTANCE_IDENTIFIER} \
    --db-parameter-group-name ${PARAMETER_GROUP_NAME} \
    --apply-immediately
```

```json
{
    "DBInstances": [
        {
            "DBInstanceIdentifier": ${DB_INSTANCE_IDENTIFIER},
            "DBInstanceClass": "db.t3.micro",
            "Engine": "mysql",
            "DBInstanceStatus": "modifying",
            ...
```

`--no-apply-immediately`를 사용하면 별도로 재시작해야 한다.

```sh
# static parameter(ex: skip-character-set-client-handshake)의 경우 pending-reboot 밖에 사용할 수 없기 때문에 재시작해야 한다.
aws rds reboot-db-instance \
    --db-instance-identifier ${DB_INSTANCE_IDENTIFIER}
```

```json
{
    "DBInstances": [
        {
            "DBInstanceIdentifier": ${DB_INSTANCE_IDENTIFIER},
            "DBInstanceClass": "db.t3.micro",
            "Engine": "mysql",
            "DBInstanceStatus": "rebooting",
            ...
        }
    ]
}
```

혹은 RDS 인스턴스를 새로 생성할 때 파라미터 그룹을 지정한다.

```sh
aws rds create-db-instance \
    --db-instance-identifier ${DB_INSTANCE_IDENTIFIER} \
    --db-instance-class db.t3.micro \
    --engine mysql \
    --engine-version 5.7 \
    --master-username admin \
    --master-user-password secret99 \
    --allocated-storage 20 \
    --db-parameter-group-name ${PARAMETER_GROUP_NAME}
```

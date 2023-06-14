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
DB_INSTANCE_IDENTIFIER="test-instance-1"
aws rds create-db-instance \
    --db-instance-identifier $DB_INSTANCE_IDENTIFIER \
    --db-instance-class db.t3.micro \
    --engine mysql \
    --master-username admin \
    --master-user-password secret99 \
    --allocated-storage 20
```

```json
// Response
{
    "DBInstance": {
        "DBInstanceIdentifier": "test-instance-1",
        "DBInstanceClass": "db.t3.micro",
        "Engine": "mysql",
        "DBInstanceStatus": "creating",
        "MasterUsername": "admin",
        "AllocatedStorage": 20,
        "PreferredBackupWindow": "16:51-17:21",
        "BackupRetentionPeriod": 1,
        "DBSecurityGroups": [],
        "VpcSecurityGroups": [
            {
                "VpcSecurityGroupId": "sg-e404358a",
                "Status": "active"
            }
        ],
        "DBParameterGroups": [
            {
                "DBParameterGroupName": "default.mysql8.0",
                "ParameterApplyStatus": "in-sync"
            }
        ],
        // ...
    }
}
```

## RDS 인스턴스 일시 중지

```sh
aws rds stop-db-instance --db-instance-identifier $DB_INSTANCE_IDENTIFIER
```

## RDS 인스턴스 시작

`start-db-instance`는 이미 생성되어 있는 인스턴스 시작하는 것임.

```sh
aws rds start-db-instance --db-instance-identifier $DB_INSTANCE_IDENTIFIER
```

```sh
aws rds describe-db-instances | jq '.[] | .[] | select(.DBInstanceIdentifier=="'"$DB_INSTANCE_IDENTIFIER"'")'
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
aws rds delete-db-instance --db-instance-identifier $DB_INSTANCE_IDENTIFIER --skip-final-snapshot
```

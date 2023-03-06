# AWS

## Troubleshooting

### CloudFormation Stack - S3 Bucket 삭제 이슈

- [ref](https://debugthis.dev/cdk/2020-07-08-aws-cdk-errors/)

S3를 임의로 삭제할 경우 다음과 같은 에러가 발생할 수 있다.

```sh
fail: No bucket named 'cdk-demo-file-assets-bucket'
```

```sh
aws s3 ls
```

위 명령어를 통해 해당 버킷이 없는 걸 확인한다.
CloudFormation에서 해당 버킷을 찾을 수 없기 때문에 에러가 발생한다.
`CDKToolkit`, `CdkDemoStack`을 삭제하고 다시 생성하면 된다.
다음 명령을 실행한다.

```sh
# aws s3api create-bucket --bucket cdk-demo-file-assets-bucket --region ap-northeast-2
# cdk bootstrap aws://<account-id>/<region>

cdk bootstrap
#  ✅  Environment aws://<account-id>/<region> bootstrapped (no changes).
```

- CloudFormation Stack을 삭제할 때 `DELETE_IN_PROGRESS` 상태에서 멈출 수도 있다.
  - [Docs](https://aws.amazon.com/ko/premiumsupport/knowledge-center/cloudformation-stack-stuck-progress/)
- CloudFormation Stack을 삭제할 때 `[role_arn] is invalid or cannot be assumed` 에러가 발생할 수 있다.
  - [Docs](https://aws.amazon.com/ko/premiumsupport/knowledge-center/cloudformation-role-arn-error/)
  - `CloudFormation` 서비스에 `IAM` 권한을 추가해야 한다.
  - 급하면 `stack_name`을 바꾸고 다시 생성한다.

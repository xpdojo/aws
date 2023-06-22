# Amazon S3

Amazon Simple Storage Service

```sh
aws list-commands
```

## S3 명령어 설명과 하위 명령어 조회

```sh
aws s3 help
```

## S3 버킷 리스팅

```sh
aws s3 ls
# 2023-06-19 15:04:14 my-s3-bucket1
# 2023-06-13 17:23:47 my-s3-bucket2
```

```sh
aws s3 ls s3://my-s3-bucket1 --recursive --human-readable --summarize
# 2023-06-21 18:04:25   86.6 MiB 12a8493d25ab35a37d8ab772702825a3c3bb834f.zip
# 2023-06-20 15:22:36   86.6 MiB 18aa72f06900cacb96ef2e1eb1bca0c1de068154.zip
# 2023-06-21 09:27:05   86.7 MiB 32dc128d378f971ee79f30152b59e057286a21cb.zip
# 2023-06-20 18:46:29   86.7 MiB 3f6fa22ffa8740aaa480785e02ab98db90c6a2af.zip
# ...
# Total Objects: 20
#    Total Size: 1.7 GiB
```

## S3 버킷 생성

```sh
aws s3 mb help
# Creates an S3 bucket.
```

- 버킷 이름을 변경하거나 다른 이름으로 시도하여 이 오류를 해결할 수 있습니다.
- 버킷 이름은 전 세계적으로 고유해야 하며, 소문자, 숫자, 하이픈(-) 및 마침표(.)만 포함할 수 있습니다.
- 또한 버킷 이름은 3~63자 사이여야 합니다.

```sh
# 흔한 이름으로 생성 시도
aws s3 mb --debug --region ap-northeast-2 s3://test-bucket
# make_bucket failed: s3://test-bucket An error occurred (BucketAlreadyExists) when calling the CreateBucket operation:
# The requested bucket name is not available.
# The bucket namespace is shared by all users of the system.
# Please select a different name and try again.
```

```sh
# 흔하지 않은 이름으로 생성 시도
aws s3 mb --debug --region ap-northeast-2 s3://zealous-almighty-having-orgulous
# make_bucket: zealous-almighty-having-orgulous
```

```sh
aws s3 ls s3://test-2f.static-site.com
                           PRE assets/
2023-06-07 13:14:16        288 error.html
2023-06-07 13:14:16        762 index.html
2023-06-07 13:14:16       1071 winipass.svg
```

```sh
aws s3 ls s3://test.bucket.name

An error occurred (NoSuchBucket) when calling the ListObjectsV2 operation: The specified bucket does not exist
```

- 이미 존재하는 버킷 이름으로 조회하면 다른 사람이 소유한 버킷이기 때문에 AccessDenied (403 Forbidden) 에러가 발생한다.
  - 그래서 혼동할 수 있지만 S3 버킷 이름은 전세계적으로 고유해야 한다는 것을 알면 쉽게 이해할 수 있다.

```sh
aws s3 ls s3://test-bucket

An error occurred (AccessDenied) when calling the ListObjectsV2 operation: Access Denied
```

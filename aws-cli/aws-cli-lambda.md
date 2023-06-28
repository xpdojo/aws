# AWS Lambda

AWS Lambda is a compute service that lets you run code without provisioning or managing servers.
([AWS](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html))

## Function 배포하기

- [Working with .zip file archives for Python Lambda functions](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html)

### Lambda execution role

서비스 역할(role)이 없다면 생성한다. ([Lambda execution role](https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html))

```sh
LAMBDA_ROLE_NAME="demo-role"
aws iam create-role \
  --role-name ${LAMBDA_ROLE_NAME} \
  --assume-role-policy-document file://Lambda-Trust.json
```

```sh
aws iam attach-role-policy \
  --role-name ${LAMBDA_ROLE_NAME} \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

```sh
aws iam attach-role-policy \
  --role-name ${LAMBDA_ROLE_NAME} \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole
```

### 압축 파일로 Function 만들기

먼저 파이썬 가상 환경(`venv`)을 설정한다.

```sh
mkdir package && cd $_
```

```sh
python3.10 -m venv venv
source venv/bin/activate
```

```python
# lambda_function.py
def lambda_handler(event, context):
  message = 'Hello {} {}!'.format(event['first_name'], event['last_name'])
  return {
      'message' : message
  }

if __name__ == '__main__':
    lambda_handler(None, None)
```

배포할 파일을 압축한다.

```sh
zip demo-lambda.zip lambda_function.py
```

### Lambda 생성

```sh
FUNCTION_NAME="demo-function"

aws lambda create-function \
  --function-name ${FUNCTION_NAME} \
  --runtime python3.10 \
  --handler lambda_function.lambda_handler \
  --role "arn:aws:iam::123456789012:role/${LAMBDA_ROLE_NAME}" \
  --zip-file fileb://demo-lambda.zip
```

이후 코드 수정 시 아래 명령어를 사용한다.

```sh
aws lambda update-function-code \
  --function-name ${FUNCTION_NAME} \
  --zip-file fileb://demo-lambda.zip
```

### 배포한 Lambda 실행 (invoke)

`payload.json`

```json
{
  "first_name": "John",
  "last_name": "Smith"
}
```

```sh
aws lambda invoke \
  --function-name ${FUNCTION_NAME} \
  --payload fileb://payload.json \
  response.json
```

`response.json`

```json
{"message": "Hello John Smith!"}
```

Python의 경우 Lambda를 직접 invoke하지 않고,
스크립트 하단에 아래와 같은 코드를 추가하면 로컬에서 실행할 수 있다.

```python
if __name__ == '__main__':
    event = {
        'first_name': 'John',
        'last_name': 'Smith'
    }
    context = {}
    print(lambda_handler(event, context))
```

```sh
python3 lambda_function.py
```

## Function 제거

```sh
aws lambda delete-function --function-name ${FUNCTION_NAME}
```

## Layer 추가하기

- [Using layers with your Lambda function](https://docs.aws.amazon.com/lambda/latest/dg/invocation-layers.html)

### MySQL 연결을 위한 Layer

pip를 이용하여 `pymysql` 모듈을 설치한다.

```sh
mkdir python
python3 -m pip install -t ./python pymysql
zip -r pymysql.zip python
```

혹은 venv 환경에서 설치한다.

```sh
python3.10 -m venv venv
source venv/bin/activate
python3.10 -m pip install pymysql
```

```sh
mkdir python
cp -r venv/lib/python3.10/site-packages/pymysql/ python/
zip -r pymysql.zip python
```

```sh
cd -
unzip -l pymysql.zip
# ...
# python3.10/site-packages/pymysql/
```

```sh
aws lambda publish-layer-version \
    --layer-name ${LAMBDA_LAYER_NAME} \
    --description "MySQL 연결을 위한 모듈" \
    --zip-file  "fileb://pymysql.zip" \
    --compatible-runtimes python3.10
```

```json
{
    "LayerVersionArn": "arn:aws:lambda:ap-northeast-2:123456789012:layer:${LAMBDA_LAYER_NAME}:1",
}
```

이미 있는 layer-name을 publish 하면 version이 올라간다.

```json
{
    "LayerVersionArn": "arn:aws:lambda:ap-northeast-2:123456789012:layer:${LAMBDA_LAYER_NAME}:2",
}
```

Layer를 Lambda Function에 연결한다.

```sh
aws lambda update-function-configuration \
    --function-name ${FUNCTION_NAME} \
    --layers arn:aws:lambda:ap-northeast-2:123456789012:layer:${LAMBDA_LAYER_NAME}:2
```

> Layer 뿐만 아니라 RDS 접근을 위한 VPC, Security Group 등을 설정해야 한다.

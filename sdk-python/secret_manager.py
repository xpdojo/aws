import boto3
from botocore.exceptions import ClientError

"""_summary_
python3 aws_secret_manager.py
> {"sendgrid_api_key":"my-api-key"}
"""


def get_secret(secret_name, region_name="ap-northeast-2"):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response["SecretString"]
    return secret


if __name__ == "__main__":
    sendgrid_api_key = get_secret(secret_name="sendgrid-secret")
    megabird_api_key = get_secret(secret_name="megabird-secret")

    print(sendgrid_api_key)
    print(megabird_api_key)

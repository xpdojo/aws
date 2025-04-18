import json
from datetime import datetime

import boto3

session = boto3.session.Session()
# sqs_resource = session.resource("sqs")
sqs_client = session.client("sqs")


def generate_message_body(company_name):
    """_summary_
    
    메시지 내용 생성
    
    Args:
        company_name (_type_, optional): 사용자 회사명.

    Returns:
        str: 메시지 내용.
    """
    if company_name is None:
        return

    now = datetime.now()
    current_time = now.strftime("%Y-%m-%dT%H:%M:%S %p")
    print(f"current_time: {current_time}")
    return json.dumps(
        {
            "messageCode": "e1ac521b-7bd8-4938-823f-438875159534",
            "receiverCompanyName": company_name,
            "receiverEmails": ["imcxsu@gmail.com", "cs.im@markruler.com"],
            "receiverPhoneNumbers": ["010-1234-5678"],
            "eventDateTime": current_time,
        },
        ensure_ascii=False,
    )


def main(queue_url):
    for _ in range(10):
        message_body = generate_message_body(company_name="테스트 회사 1")
        res = sqs_client.send_message(QueueUrl=queue_url, MessageBody=message_body)
        print(f"sqs_client.send_message.response: {res}")

    for _ in range(5):
        message_body = generate_message_body(company_name="테스트 회사 2")
        res = sqs_client.send_message(QueueUrl=queue_url, MessageBody=message_body)
        print(f"sqs_client.send_message.response: {res}")


if __name__ == "__main__":
    main(
        queue_url="https://sqs.ap-northeast-2.amazonaws.com/$USER_ID/$QUEUE_NAME",
    )

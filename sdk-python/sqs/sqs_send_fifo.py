import json
import uuid

import boto3

session = boto3.session.Session()
sqs_client = session.client("sqs")

QUEUE_URL = "https://sqs.ap-northeast-2.amazonaws.com/$USER_ID/$QUEUE_NAME"
MESSAGE_GROUP_ID = "something-unique"
BODY = {}


def generate_message_body():
    """_summary_
    
    메시지 내용 생성

    Returns:
        str: 메시지 내용.
    """
    return json.dumps(BODY, ensure_ascii=False)


def main():
    message_body = generate_message_body()
    print(f"message_body: {message_body}")
    res = sqs_client.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=message_body,
        MessageGroupId=MESSAGE_GROUP_ID,  # 메시지 순서를 보장하기 위한 그룹 ID
        MessageDeduplicationId=str(uuid.uuid4())  # 중복 방지를 위한 고유 ID
    )
    print(f"sqs_client.send_message.response: {res}")


if __name__ == "__main__":
    main()

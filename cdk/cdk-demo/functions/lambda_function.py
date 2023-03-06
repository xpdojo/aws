import logging
import smtplib
from datetime import datetime, timezone, timedelta

import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# CLI 실행 시
# pytest --log-cli-level=DEBUG

KST = timezone(timedelta(hours=9), name='KST')


def convert_event_time(event_time: str) -> datetime:
    strptime = datetime.strptime(event_time, "%Y-%m-%dT%H:%M:%SZ")
    return strptime.astimezone(tz=KST)


def send_gmail(sender: str,
               recipients: list[str]):
    # SMTP 서버 설정
    smtp_server = "smtp.gmail.com"
    port = 587  # TLS: 587, SSL: 465, SMTP: 25
    password = "password"  # 발신자 이메일의 비밀번호

    # 이메일 생성
    subject = "Good morning!"  # 이메일 제목
    body = "Hello, Good morning!"  # 이메일 본문

    # 이메일 보내기
    message = f"""\
    Subject: {subject}
    To: {','.join(recipients)}
    From: {sender}
    Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

    {body}
    """
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()

        # auth
        server.starttls()
        server.login(sender, password)

        server.sendmail(from_addr=sender, to_addrs=recipients, msg=message)


def send_ses(sender: str,
             recipients: list[str]):
    client = boto3.client('ses')

    ses_response = client.send_email(
        Source=sender,
        Destination={
            'ToAddresses': recipients
        },
        Message={
            'Subject': {
                'Data': 'Hello from AWS CDK!',
                'Charset': 'UTF-8',
            },
            'Body': {
                'Text': {
                    'Data': 'This is a test email sent using AWS CDK and Amazon SES.',
                    'Charset': 'UTF-8',
                },
            }
        }
    )

    logger.info(f"ses response id received: {ses_response['MessageId']}.")


def handler(event: dict, context=None):
    # logging.info(f"Call Lambda at {datetime.now(tz=KST).strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("event: %s", event)
    logger.info("context: %s", type(context))
    logger.info("context: %s", context)

    # send_gmail()
    send_ses(
        sender="imcxsu@gmail.com",
        recipients=[
        "imcxsu@gmail.com",
    ])

    logger.info("Full event: %s", event)

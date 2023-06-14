# SQS

```sh
aws configure list-profiles
```

```sh
aws list-commands
```

## SQS 명령어 설명과 하위 명령어 조회

```sh
aws sqs help
```

## 대기열 목록

```sh
aws sqs list-queues
```

```json
{
    "QueueUrls": [
        "https://sqs.ap-northeast-2.amazonaws.com/092740280445/Autowini_CarDetailsLog",
        "https://sqs.ap-northeast-2.amazonaws.com/092740280445/Autowini_ItemDetailsUpdate.fifo",
        "https://sqs.ap-northeast-2.amazonaws.com/092740280445/Autowini_SalesStatusUpdate",
        "https://sqs.ap-northeast-2.amazonaws.com/092740280445/Autowini_TruckDetailsLog",
        "https://sqs.ap-northeast-2.amazonaws.com/092740280445/auctionwini-image-convert-queue",
        "https://sqs.ap-northeast-2.amazonaws.com/092740280445/auctionwini-server-call-queue",
        "https://sqs.ap-northeast-2.amazonaws.com/092740280445/winipass-queue-dev"
    ]
}
```

## 메시지 보내기

```sh
# aws sqs send-message --queue-url <queue-url> --message-body <message-body>
aws sqs send-message \
  --queue-url "https://sqs.ap-northeast-2.amazonaws.com/092740280445/winipass-queue-dev" \
  --message-body "Hello World"
```

```json
{
    "MD5OfMessageBody": "9ac12c909a0325d55d487543bac18716",
    "MessageId": "573bb4bf-a9eb-48b2-9ad7-3408a3bb1ac3"
}
```

## 메시지 폴링

```sh
# aws sqs receive-message --queue-url <queue-url>
aws sqs receive-message --queue-url https://sqs.ap-northeast-2.amazonaws.com/092740280445/winipass-queue-dev
```

```json
{
    "Messages": [
        {
            "MessageId": "c66eae44-4612-4166-b883-efb6976f6a4e",
            "ReceiptHandle": "AQEB4JPoKuRBtgJrxL6fLHoQ3RhUY32dcNXwhqQzRQD5cl6cnDbO/Hceq6qnRzCMIhsOjhzO+GBBERWNMbogRTzdVQoTL6DGRUjXiCbhT2ARMxXmFoOmVbSvF1qg60upkNLmf58T6RSHeIwl9tm2FaWSJ3SQKFDnsuajJstucUEi7Hm7WULFrFMrTvLdMmLq9vmZb4LrEZskEX3KoGsaLdGxUHKbU9mU837UNL6I84jbhZMngXSpW/D4mX1M6gUEGVsLbUPS/IlLvMLNeSBKsw1S+8V2+IIuq8Rtg4roFcZHJzcwTbImOmTbSS5sbS65f5IAVd1xV0TdwpbvqBq/Ydxs/UtjRbRHw2S7LMKhNH/COwaOJGMnabkbbu5phwwbhraSQBHk8RBE5mvqp0RbkAUup7A7hACwbS3ahPRpU8qjv6I=",
            "MD5OfBody": "86fb269d190d2c85f6e0468ceca42a20",
            "Body": "Hello world!"
        }
    ]
}
```

메시지를 폴링한 후 처리가 완료되면, 메시지를 삭제해야 한다.
삭제하지 않은 경우, 동일한 메시지가 계속해서 폴링된다.
메시지를 삭제하기 위해서는 다음 명령을 사용한다.

```sh
# aws sqs delete-message --queue-url <queue-url> --receipt-handle <receipt-handle>
aws sqs delete-message --queue-url https://sqs.ap-northeast-2.amazonaws.com/092740280445/winipass-queue-dev --receipt-handle AQEB4JPoKuRBtgJrxL6fLHoQ3RhUY32dcNXwhqQzRQD5cl6cnDbO/Hceq6qnRzCMIhsOjhzO+GBBERWNMbogRTzdVQoTL6DGRUjXiCbhT2ARMxXmFoOmVbSvF1qg60upkNLmf58T6RSHeIwl9tm2FaWSJ3SQKFDnsuajJstucUEi7Hm7WULFrFMrTvLdMmLq9vmZb4LrEZskEX3KoGsaLdGxUHKbU9mU837UNL6I84jbhZMngXSpW/D4mX1M6gUEGVsLbUPS/IlLvMLNeSBKsw1S+8V2+IIuq8Rtg4roFcZHJzcwTbImOmTbSS5sbS65f5IAVd1xV0TdwpbvqBq/Ydxs/UtjRbRHw2S7LMKhNH/COwaOJGMnabkbbu5phwwbhraSQBHk8RBE5mvqp0RbkAUup7A7hACwbS3ahPRpU8qjv6I=
```

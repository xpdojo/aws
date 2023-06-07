package com.demo.sqs;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import software.amazon.awssdk.services.sqs.SqsClient;
import software.amazon.awssdk.services.sqs.model.CreateQueueRequest;
import software.amazon.awssdk.services.sqs.model.GetQueueUrlRequest;
import software.amazon.awssdk.services.sqs.model.GetQueueUrlResponse;
import software.amazon.awssdk.services.sqs.model.ListQueuesRequest;
import software.amazon.awssdk.services.sqs.model.ListQueuesResponse;
import software.amazon.awssdk.services.sqs.model.QueueAttributeName;
import software.amazon.awssdk.services.sqs.model.SendMessageRequest;
import software.amazon.awssdk.services.sqs.model.SendMessageResponse;

import javax.annotation.PostConstruct;
import java.util.HashMap;

@Slf4j
@RequiredArgsConstructor
@Component
public class SqsPublisher {

    private final SqsClient sqsClient;

    @PostConstruct
    void init() {
        testClient();
    }

    public void testClient() {
        final var queueName = "test-queue-dev";
        // createQueue(queueName);

        GetQueueUrlResponse queueUrl = findQueueUrlByName(queueName);
        // listQueue(queueName);

        final var message = "Hello world!";
        sendMessage(queueUrl, message);

        sqsClient.close();
    }

    /**
     * 대기열을 검색한다.
     *
     * @param queueName 대기열 이름
     * @return 대기열 URL
     */
    private GetQueueUrlResponse findQueueUrlByName(String queueName) {
        // Get the URL for a queue
        GetQueueUrlRequest getQueueUrlRequest =
                GetQueueUrlRequest.builder()
                        .queueName(queueName)
                        .build();
        GetQueueUrlResponse queueUrl = sqsClient.getQueueUrl(getQueueUrlRequest);
        log.debug("queueUrl={}", queueUrl);

        return queueUrl;
    }

    /**
     * 대기열 이름으로 시작하는 대기열 목록을 가져온다.
     *
     * @param queueName 대기열 이름
     */
    private void listQueue(final String queueName) {
        ListQueuesRequest listQueuesRequest =
                ListQueuesRequest.builder()
                        .queueNamePrefix(queueName)
                        .build();
        ListQueuesResponse listQueuesResponse = sqsClient.listQueues(listQueuesRequest);
        for (String url : listQueuesResponse.queueUrls()) {
            log.debug("listQueueUrl={}", url);
        }
    }

    /**
     * 대기열에 메시지를 보낸다.
     *
     * @param queueUrl 대기열 URL
     * @param message  메시지
     */
    private void sendMessage(GetQueueUrlResponse queueUrl, String message) {
        SendMessageRequest sendMessage =
                SendMessageRequest.builder()
                        .queueUrl(queueUrl.queueUrl())
                        .messageBody(message)
                        .build();

        SendMessageResponse sendMessageResponse = sqsClient.sendMessage(sendMessage);
        log.debug("sendMessageResponse={}", sendMessageResponse);
    }

    /**
     * Amazon SQS 대기열(queue)을 생성한다.
     * Queue(대기열)를 직접 생성했다면 상관없다.
     *
     * @deprecated Queue 생성은 콘솔에서 미리 할 것
     */
    @Deprecated
    public String createQueue(String queueName) {
        CreateQueueRequest createQueueRequest =
                CreateQueueRequest.builder()
                        .queueName(queueName)
                        .attributes(
                                new HashMap<>() {
                                    {
                                        put(QueueAttributeName.DELAY_SECONDS, "60");
                                        put(QueueAttributeName.MESSAGE_RETENTION_PERIOD, "86400");
                                    }
                                }
                        )
                        .build();

        sqsClient.createQueue(createQueueRequest);

        GetQueueUrlResponse getQueueUrlResponse = sqsClient.getQueueUrl(GetQueueUrlRequest.builder().queueName(queueName).build());
        return getQueueUrlResponse.queueUrl();
    }

}

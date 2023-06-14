package com.demo.sqs;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import software.amazon.awssdk.services.sqs.SqsClient;
import software.amazon.awssdk.services.sqs.model.GetQueueUrlResponse;
import software.amazon.awssdk.services.sqs.model.QueueAttributeName;
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
        log.debug("queueUrl={}", queueUrl);
        // listQueue(queueName);

        final var message = "Hello world!";
        SendMessageResponse sendMessageResponse = sendMessage(queueUrl, message);
        log.debug("sendMessageResponse={}", sendMessageResponse);

        sqsClient.close();
    }

    /**
     * 대기열을 검색한다.
     *
     * @param queueName 대기열 이름
     * @return 대기열 URL
     */
    private GetQueueUrlResponse findQueueUrlByName(String queueName) {
        return sqsClient.getQueueUrl(builder -> builder
                .queueName(queueName)
                .build());
    }

    /**
     * 대기열 이름으로 시작하는 대기열 목록을 가져온다.
     *
     * @param queueName 대기열 이름
     */
    private void listQueue(final String queueName) {
        var response =
                sqsClient.listQueues(builder -> builder
                        .queueNamePrefix(queueName)
                        .build());

        for (String url : response.queueUrls()) {
            log.debug("listQueueUrl={}", url);
        }
    }

    /**
     * 대기열에 메시지를 보낸다.
     *
     * @param queueUrl 대기열 URL
     * @param message  메시지
     */
    private SendMessageResponse sendMessage(GetQueueUrlResponse queueUrl, String message) {
        return sqsClient.sendMessage(builder -> builder
                .queueUrl(queueUrl.queueUrl())
                .messageBody(message)
                .build());
    }

    /**
     * Amazon SQS 대기열(queue)을 생성한다.
     * Queue(대기열)를 직접 생성했다면 상관없다.
     *
     * @deprecated Queue 생성은 콘솔에서 미리 할 것
     */
    @Deprecated
    public String createQueue(String queueName) {
        return sqsClient.createQueue(builder -> builder
                        .queueName(queueName)
                        .attributes(
                                new HashMap<>() {
                                    {
                                        put(QueueAttributeName.DELAY_SECONDS, "60");
                                        put(QueueAttributeName.MESSAGE_RETENTION_PERIOD, "86400");
                                    }
                                }
                        )
                        .build())
                .queueUrl();
    }

}

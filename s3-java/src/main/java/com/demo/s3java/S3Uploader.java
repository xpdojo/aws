package com.demo.s3java;


import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.GetBucketLocationResponse;
import software.amazon.awssdk.services.s3.model.PutObjectResponse;

import javax.annotation.PostConstruct;
import java.io.IOException;
import java.util.UUID;

/**
 * S3 파일 업로더
 */
@Slf4j
@RequiredArgsConstructor
@Component
public class S3Uploader {

    private final S3Client client;

    /**
     * 버킷 이름은 전 세계적으로 고유해야 한다.
     * 소문자, 숫자, 하이픈(-) 및 마침표(.)만 포함할 수 있다.
     *
     * 만약 전세계를 기준으로 이미 있는 버킷 이름이라면 BucketAlreadyExists이 발생한다.
     * 해당 버킷을 조회하면 다른 사람이 생성한 버킷이기 때문에 Access Denied (403 Forbidden) 에러가 발생해서 혼동할 수 있다.
     */
    @Value("${cloud.aws.s3.bucket}")
    private String bucket;

    @PostConstruct
    public void init() {
        log.debug("S3Uploader init");
        // CreateBucketResponse createBucketResponse = client.createBucket(builder -> builder.bucket(bucket).build());
        // log.debug("createBucketResponse: {}", createBucketResponse);

        GetBucketLocationResponse bucketLocation = client.getBucketLocation(builder -> builder.bucket(bucket).build());
        log.debug("bucketLocation: {}", bucketLocation);

        upload("""
                test/subdir/%s.txt
                """.formatted(UUID.randomUUID().toString()));
    }

    /**
     * S3 버킷에 파일을 업로드한다.
     *
     * @param filePath 파일을 저장할 경로
     * @return 업로드 성공 여부
     */
    public boolean upload(final String filePath) {
        RequestBody requestBody = RequestBody.fromBytes("이것은 내용입니다.".getBytes());

        PutObjectResponse putObjectResponse = client.putObject(builder -> builder
                .bucket(bucket)
                .key(filePath)
                // .contentType(multipartFile.getContentType())
                // .contentLength(multipartFile.getSize())
                .build(), requestBody);

        return putObjectResponse.sdkHttpResponse().isSuccessful();
    }

    /**
     * 다운로드
     */
    public byte[] download(String path) throws IOException {
        return client
                .getObject(builder -> builder.bucket(bucket).key(path))
                .readAllBytes();
    }

}

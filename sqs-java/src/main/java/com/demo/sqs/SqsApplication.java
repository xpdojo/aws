package com.demo.sqs;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import software.amazon.awssdk.auth.credentials.ContainerCredentialsProvider;
import software.amazon.awssdk.auth.credentials.DefaultCredentialsProvider;
import software.amazon.awssdk.auth.credentials.EnvironmentVariableCredentialsProvider;
import software.amazon.awssdk.auth.credentials.InstanceProfileCredentialsProvider;
import software.amazon.awssdk.auth.credentials.ProfileCredentialsProvider;
import software.amazon.awssdk.auth.credentials.SystemPropertyCredentialsProvider;
import software.amazon.awssdk.auth.credentials.WebIdentityTokenFileCredentialsProvider;
import software.amazon.awssdk.core.SdkSystemSetting;
import software.amazon.awssdk.profiles.ProfileFile;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.sqs.SqsClient;

@SpringBootApplication
public class SqsApplication {

    public static void main(String[] args) {
        SpringApplication.run(SqsApplication.class, args);
    }

    // Create a SqsClient object
    @Bean
    public SqsClient sqsClient() {
        return SqsClient.builder()
                .region(Region.AP_NORTHEAST_2)
                /**
                 * AWS credentials provider chain that looks for credentials in this order:
                 * <ol>
                 *   <li>Java System Properties - {@code aws.accessKeyId} and {@code aws.secretAccessKey}</li>
                 *   <li>Environment Variables - {@code AWS_ACCESS_KEY_ID} and {@code AWS_SECRET_ACCESS_KEY}</li>
                 *   <li>Web Identity Token credentials from system properties or environment variables</li>
                 *   <li>Credential profiles file at the default location (~/.aws/credentials) shared by all AWS SDKs and the AWS CLI</li>
                 *   <li>Credentials delivered through the Amazon EC2 container service if AWS_CONTAINER_CREDENTIALS_RELATIVE_URI" environment
                 *   variable is set and security manager has permission to access the variable,</li>
                 *   <li>Instance profile credentials delivered through the Amazon EC2 metadata service</li>
                 * </ol>
                 *
                 * @see SystemPropertyCredentialsProvider
                 * @see EnvironmentVariableCredentialsProvider
                 * @see ProfileCredentialsProvider
                 * @see WebIdentityTokenFileCredentialsProvider
                 * @see ContainerCredentialsProvider
                 * @see InstanceProfileCredentialsProvider
                 */
                .credentialsProvider(DefaultCredentialsProvider.create())
                /**
                 * Credentials provider based on AWS configuration profiles. This loads credentials from a {@link ProfileFile}, allowing you to
                 * share multiple sets of AWS security credentials between different tools like the AWS SDK for Java and the AWS CLI.
                 *
                 * <p>See http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html</p>
                 *
                 * <p>If this credentials provider is loading assume-role credentials from STS, it should be cleaned up with {@link #close()} if
                 * it is no longer being used.</p>
                 *
                 * @see ProfileFile
                 */
                // .credentialsProvider(ProfileCredentialsProvider.create()) // 로컬 구성 ($HOME/.aws/credentials)
                /**
                 * Credentials provider implementation that loads credentials from the Amazon EC2 Instance Metadata Service.
                 *
                 * <P>
                 * If {@link SdkSystemSetting#AWS_EC2_METADATA_DISABLED} is set to true, it will not try to load
                 * credentials from EC2 metadata service and will return null.
                 */
                // .credentialsProvider(InstanceProfileCredentialsProvider.create()) // EC2 인스턴스 프로파일
                .build();
    }

}

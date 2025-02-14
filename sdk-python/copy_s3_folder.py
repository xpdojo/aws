import logging
from pprint import pprint

import boto3
from botocore.exceptions import ClientError

"""
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
https://docs.aws.amazon.com/ko_kr/AmazonS3/latest/userguide/service_code_examples_actions.html
https://github.com/awsdocs/aws-doc-sdk-examples/blob/main/python/example_code/s3/s3_basics/object_wrapper.py
"""
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Purpose
Show how to use AWS SDK for Python (Boto3) with Amazon Simple Storage Service
(Amazon S3) to perform basic object operations
"""

logger = logging.getLogger(__name__)
BUCKET_NAME = 'your_bucket'


# snippet-start:[python.example_code.s3.helper.ObjectWrapper]
class ObjectWrapper:
    """Encapsulates S3 object actions."""

    def __init__(self, s3_object):
        """
        :param s3_object: A Boto3 Object resource. This is a high-level resource in Boto3
                          that wraps object actions in a class-like structure.
        """
        self.object = s3_object
        self.key = self.object.key

    # snippet-end:[python.example_code.s3.helper.ObjectWrapper]

    # snippet-start:[python.example_code.s3.PutObject]
    def put(self, data):
        """
        Upload data to the object.

        :param data: The data to upload. This can either be bytes or a string. When this
                     argument is a string, it is interpreted as a file name, which is
                     opened in read bytes mode.
        """
        put_data = data
        if isinstance(data, str):
            try:
                put_data = open(data, 'rb')
            except IOError:
                logger.exception("Expected file name or binary data, got '%s'.", data)
                raise

        try:
            self.object.put(Body=put_data)
            self.object.wait_until_exists()
            logger.info(
                "Put object '%s' to bucket '%s'.", self.object.key,
                self.object.BUCKET_NAME)
        except ClientError:
            logger.exception(
                "Couldn't put object '%s' to bucket '%s'.", self.object.key,
                self.object.BUCKET_NAME)
            raise
        finally:
            if getattr(put_data, 'close', None):
                put_data.close()

    # snippet-end:[python.example_code.s3.PutObject]

    # snippet-start:[python.example_code.s3.GetObject]
    def get(self):
        """
        Gets the object.

        :return: The object data in bytes.
        """
        try:
            body = self.object.get()['Body'].read()
            logger.info(
                "Got object '%s' from bucket '%s'.",
                self.object.key, self.object.BUCKET_NAME)
        except ClientError:
            logger.exception(
                "Couldn't get object '%s' from bucket '%s'.",
                self.object.key, self.object.BUCKET_NAME)
            raise
        else:
            return body

    # snippet-end:[python.example_code.s3.GetObject]

    # snippet-start:[python.example_code.s3.ListObjects]
    @staticmethod
    def list(bucket, prefix=None):
        """
        Lists the objects in a bucket, optionally filtered by a prefix.

        :param bucket: The bucket to query. This is a Boto3 Bucket resource.
        :param prefix: When specified, only objects that start with this prefix are listed.
        :return: The list of objects.
        """
        try:
            if not prefix:
                objects = list(bucket.objects.all())
            else:
                objects = list(bucket.objects.filter(Prefix=prefix))
            logger.info("Got objects %s from bucket '%s'",
                        [o.key for o in objects], bucket.name)
        except ClientError:
            logger.exception("Couldn't get objects for bucket '%s'.", bucket.name)
            raise
        else:
            return objects

    # snippet-end:[python.example_code.s3.ListObjects]

    # snippet-start:[python.example_code.s3.CopyObject]
    def copy(self, dest_object):
        """
        Copies the object to another bucket.

        :param dest_object: The destination object initialized with a bucket and key.
                            This is a Boto3 Object resource.
        """
        try:
            dest_object.copy_from(CopySource={
                'Bucket': self.object.BUCKET_NAME,
                'Key': self.object.key
            })
            dest_object.wait_until_exists()
            logger.info(
                "Copied object from %s:%s to %s:%s.",
                self.object.BUCKET_NAME, self.object.key,
                dest_object.BUCKET_NAME, dest_object.key)
        except ClientError:
            logger.exception(
                "Couldn't copy object from %s/%s to %s/%s.",
                self.object.BUCKET_NAME, self.object.key,
                dest_object.BUCKET_NAME, dest_object.key)
            raise

    # snippet-end:[python.example_code.s3.CopyObject]

    # snippet-start:[python.example_code.s3.DeleteObject]
    def delete(self):
        """
        Deletes the object.
        """
        try:
            self.object.delete()
            self.object.wait_until_not_exists()
            logger.info(
                "Deleted object '%s' from bucket '%s'.",
                self.object.key, self.object.BUCKET_NAME)
        except ClientError:
            logger.exception(
                "Couldn't delete object '%s' from bucket '%s'.",
                self.object.key, self.object.BUCKET_NAME)
            raise

    # snippet-end:[python.example_code.s3.DeleteObject]

    # snippet-start:[python.example_code.s3.DeleteObjects_Keys]
    @staticmethod
    def delete_objects(bucket, object_keys):
        """
        Removes a list of objects from a bucket.
        This operation is done as a batch in a single request.

        :param bucket: The bucket that contains the objects. This is a Boto3 Bucket
                       resource.
        :param object_keys: The list of keys that identify the objects to remove.
        :return: The response that contains data about which objects were deleted
                 and any that could not be deleted.
        """
        try:
            response = bucket.delete_objects(Delete={
                'Objects': [{
                    'Key': key
                } for key in object_keys]
            })
            if 'Deleted' in response:
                logger.info(
                    "Deleted objects '%s' from bucket '%s'.",
                    [del_obj['Key'] for del_obj in response['Deleted']], bucket.name)
            if 'Errors' in response:
                logger.warning(
                    "Could not delete objects '%s' from bucket '%s'.", [
                        f"{del_obj['Key']}: {del_obj['Code']}"
                        for del_obj in response['Errors']],
                    bucket.name)
        except ClientError:
            logger.exception("Couldn't delete any objects from bucket %s.", bucket.name)
            raise
        else:
            return response

    # snippet-end:[python.example_code.s3.DeleteObjects_Keys]

    # snippet-start:[python.example_code.s3.DeleteObjects_All]
    @staticmethod
    def empty_bucket(bucket):
        """
        Remove all objects from a bucket.

        :param bucket: The bucket to empty. This is a Boto3 Bucket resource.
        """
        try:
            bucket.objects.delete()
            logger.info("Emptied bucket '%s'.", bucket.name)
        except ClientError:
            logger.exception("Couldn't empty bucket '%s'.", bucket.name)
            raise

    # snippet-end:[python.example_code.s3.DeleteObjects_All]

    # snippet-start:[python.example_code.s3.PutObjectAcl]
    def put_acl(self, email):
        """
        Applies an ACL to the object that grants read access to an AWS user identified
        by email address.

        :param email: The email address of the user to grant access.
        """
        try:
            acl = self.object.Acl()
            # Putting an ACL overwrites the existing ACL, so append new grants
            # if you want to preserve existing grants.
            grants = acl.grants if acl.grants else []
            grants.append({
                'Grantee': {
                    'Type': 'AmazonCustomerByEmail',
                    'EmailAddress': email
                },
                'Permission': 'READ'
            })
            acl.put(
                AccessControlPolicy={
                    'Grants': grants,
                    'Owner': acl.owner
                }
            )
            logger.info("Granted read access to %s.", email)
        except ClientError:
            logger.exception("Couldn't add ACL to object '%s'.", self.object.key)
            raise

    # snippet-end:[python.example_code.s3.PutObjectAcl]

    # snippet-start:[python.example_code.s3.GetObjectAcl]
    def get_acl(self):
        """
        Gets the ACL of the object.

        :return: The ACL of the object.
        """
        try:
            acl = self.object.Acl()
            logger.info(
                "Got ACL for object %s owned by %s.",
                self.object.key, acl.owner['DisplayName'])
        except ClientError:
            logger.exception("Couldn't get ACL for object %s.", self.object.key)
            raise
        else:
            return acl


# snippet-end:[python.example_code.s3.GetObjectAcl]


def copy_and_delete_s3_object():
    print('-' * 88)
    print("Amazon S3 object를 새로운 key로 복사하고 기존 오브젝트(Key)를 삭제한다.")
    print('-' * 88)

    session = boto3.Session(profile_name='default')
    print(type(session))
    print(f'available_profile={session.available_profiles}')
    print(dir(session))
    print(session.get_credentials().access_key)
    print(session.get_credentials().secret_key)
    print(session.get_available_resources())

    s3_ = 's3'
    s3_resource = session.resource(s3_)
    bucket_ = s3_resource.Bucket(bucket_name)
    s3_client = session.client(s3_)
    objects = s3_client.list_objects(Bucket=bucket_name)

    contents = objects['Contents']
    for content in contents:
        pprint(content)

        # check object key
        key_: str = content['Key']
        if key_.startswith('guides/') \
                or key_.endswith('/') \
                or "EXP23" in key_:
            print('skip')
            continue

        # generate new key
        split = key_.split('/')
        new_key_ = f"export-documents/EXP{content['LastModified'].strftime('%y%m%d')}{split[1].replace('-', '').upper()[0:10]}/{split[2]}"
        print(new_key_)

        # copy s3 object
        source_object = {
            'Bucket': bucket_name,
            'Key': key_
        }
        response = s3_resource.meta.client.copy(
            source_object,
            bucket_name,
            new_key_)
        print(type(response))
        print(response)

        # delete s3 object
        # ObjectWrapper.delete_objects(bucket_, key_)
        s3_client.delete_object(Bucket=bucket_name, Key=key_)

    listed_lines = ObjectWrapper.list(bucket_)
    print(f"Their keys are: {', '.join(l.key for l in listed_lines)}")


if __name__ == '__main__':
    copy_and_delete_s3_object()

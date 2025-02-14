from collections import defaultdict
from pprint import pprint

import boto3

BUCKET_NAME = 'your_bucket'
KEY_PREFIX = 'videos/B2025'


def get_folder_sizes(bucket_name):
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    folder_sizes = defaultdict(lambda: {'size': 0, 'last_modified': None})

    for page in paginator.paginate(Bucket=bucket_name):
        if 'Contents' not in page:
            print("No contents found in the bucket.")
            continue
        for obj in page.get('Contents', []):
            if obj['Key'].startswith(KEY_PREFIX):
                folder = obj['Key']
                folder_sizes[folder]['size'] += obj['Size']
                if folder_sizes[folder]['last_modified'] is None or obj['LastModified'] > folder_sizes[folder][
                    'last_modified']:
                    folder_sizes[folder]['last_modified'] = obj['LastModified']

    if not folder_sizes:
        print("No video folder found.")
    sorted_folders = sorted(folder_sizes.items(), key=lambda x: x[1]['size'], reverse=True)
    return sorted_folders


def list_incomplete_multipart_uploads(bucket_name):
    s3 = boto3.client('s3')
    incomplete_uploads = []

    paginator = s3.get_paginator('list_multipart_uploads')
    for page in paginator.paginate(Bucket=bucket_name):
        if 'Uploads' in page:
            for upload in page['Uploads']:
                incomplete_uploads.append({
                    'Key': upload['Key'],
                    'UploadId': upload['UploadId'],
                    'Initiated': upload['Initiated']
                })

    return incomplete_uploads


if __name__ == '__main__':
    folder_sizes = get_folder_sizes(BUCKET_NAME)
    if not folder_sizes:
        print("No folders to display.")
    for folder, info in folder_sizes:
        size_mib = info['size'] / (1024 * 1024)
        pprint(
            f'Folder: {folder}, Size: {info["size"]} bytes ({size_mib:.2f} MiB), Last Modified: {info["last_modified"]}')

    incomplete_uploads_list = list_incomplete_multipart_uploads(BUCKET_NAME)
    if not incomplete_uploads_list:
        print("No incomplete multipart uploads found.")
    else:
        print("⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠ Incomplete multipart uploads:")
        for incomplete_upload in incomplete_uploads_list:
            pprint(
                f'Key: {incomplete_upload["Key"]}, UploadId: {incomplete_upload["UploadId"]}, Initiated: {incomplete_upload["Initiated"]}')

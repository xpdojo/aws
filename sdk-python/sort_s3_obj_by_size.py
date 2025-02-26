from collections import defaultdict
from pprint import pprint
import datetime

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
    # 스크립트 이름과 현재 날짜/시간을 포함한 로그 파일 생성
    current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    log_filename = __file__.replace('.py', f'-{current_datetime}.log')
    
    with open(log_filename, 'w') as log_file:
        folder_sizes = get_folder_sizes(BUCKET_NAME)
        if not folder_sizes:
            log_file.write("No folders to display.\n")
        for folder, info in folder_sizes:
            size_mib = info['size'] / (1024 * 1024)
            log_message = f'Folder: {folder}, Size: {info["size"]} bytes ({size_mib:.2f} MiB), Last Modified: {info["last_modified"]}\n'
            log_file.write(log_message)
            print(log_message, end='')  # 콘솔에도 출력

        incomplete_uploads_list = list_incomplete_multipart_uploads(BUCKET_NAME)
        if not incomplete_uploads_list:
            log_file.write("No incomplete multipart uploads found.\n")
        else:
            warning_message = "⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠ Incomplete multipart uploads:\n"
            log_file.write(warning_message)
            print(warning_message, end='')
            for incomplete_upload in incomplete_uploads_list:
                log_message = f'Key: {incomplete_upload["Key"]}, UploadId: {incomplete_upload["UploadId"]}, Initiated: {incomplete_upload["Initiated"]}\n'
                log_file.write(log_message)
                print(log_message, end='')

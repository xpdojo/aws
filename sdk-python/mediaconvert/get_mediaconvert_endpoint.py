import boto3

mediaconvert_client = boto3.client('mediaconvert')
endpoints = mediaconvert_client.describe_endpoints()
endpoint_url = endpoints['Endpoints'][0]['Url']
print(endpoint_url)
# https://{something}.mediaconvert.ap-northeast-2.amazonaws.com

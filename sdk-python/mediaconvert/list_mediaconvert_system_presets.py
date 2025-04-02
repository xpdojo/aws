import boto3
import json


def list_system_presets():
    # MediaConvert 클라이언트 생성
    mediaconvert = boto3.client('mediaconvert')

    # MediaConvert 서비스 엔드포인트 가져오기
    endpoints = mediaconvert.describe_endpoints()
    endpoint_url = endpoints['Endpoints'][0]['Url']

    # 엔드포인트를 지정하여 새로운 클라이언트 생성
    mediaconvert = boto3.client('mediaconvert', endpoint_url=endpoint_url)

    # 시스템 프리셋 조회
    response = mediaconvert.list_presets(
        ListBy='SYSTEM'  # 시스템 프리셋만 조회
    )

    # # 전체 프리셋 조회 (시스템 + 사용자 정의)
    # response = mediaconvert.list_presets()

    # 프리셋 목록 출력
    presets = response.get('Presets', [])
    for preset in presets:
        print("=" * 50)
        preset.pop('Arn')
        preset.pop('CreatedAt')
        preset.pop('LastUpdated')
        print(preset)


if __name__ == "__main__":
    list_system_presets()

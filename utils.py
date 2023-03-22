import base64
import requests
import json
import random
import os

CUSTOMER_KEY = os.getenv('CUSTOMER_KEY')
CUSTOMER_SECRET = os.getenv('CUSTOMER_SECRET')

TEMP_TOKEN = os.getenv('TEMP_TOKEN')
APP_ID = os.getenv('APP_ID')
CHANNEL = os.getenv('CHANNEL')
UID = random.randint(1, 232)

AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')


def generate_credential():
    # Generate encoded token based on customer key and secret
    credentials = CUSTOMER_KEY + ":" + CUSTOMER_SECRET

    base64_credentials = base64.b64encode(credentials.encode("utf8"))
    credential = base64_credentials.decode("utf8")
    return credential


credential = generate_credential()


def generate_resource():

    payload = {
        "cname": CHANNEL,
        "uid": str(UID),
        "clientRequest": {}
    }

    headers = {}

    headers['Authorization'] = 'basic ' + credential

    headers['Content-Type'] = 'application/json'

    url = f"https://api.agora.io/v1/apps/{APP_ID}/cloud_recording/acquire"
    res = requests.post(url, headers=headers, data=json.dumps(payload))

    data = res.json()
    resourceId = data["resourceId"]

    return resourceId

# generate_resource()


def start_call():
    resource_id = generate_resource()
    print('resource_id')
    url = f"https://api.agora.io/v1/apps/{APP_ID}/cloud_recording/resourceid/{resource_id}/mode/mix/start"
    payload = {
        "cname": CHANNEL,
        "uid": str(UID),
        "clientRequest": {
            "token": TEMP_TOKEN,

            "recordingConfig": {
                "maxIdleTime": 3,
            },

            "storageConfig": {
                "secretKey": AWS_SECRET_KEY,
                "vendor": 1,  # 1 is for AWS
                "region": 3,
                "bucket": AWS_BUCKET_NAME,
                "accessKey": AWS_ACCESS_KEY,
                "fileNamePrefix": [
                    "agora",
                ]
            },

            "recordingFileConfig": {
                "avFileType": [
                    "hls",
                    "mp4"
                ]
            },
        },
    }

    headers = {}

    headers['Authorization'] = 'basic ' + credential

    headers['Content-Type'] = 'application/json'

    res = requests.post(url, headers=headers, data=json.dumps(payload))
    data = res.json()
    sid = data["sid"]

    return resource_id, sid


def stop_call(resource_id, sid):
    print('resource_id:', resource_id)
    url = f"https://api.agora.io/v1/apps/{APP_ID}/cloud_recording/resourceid/{resource_id}/sid/{sid}/mode/mix/stop"

    headers = {}

    headers['Authorization'] = 'basic ' + credential

    headers['Content-Type'] = 'application/json'

    payload = {
        "cname": "main",
        "uid": str(UID),
        "clientRequest": {
        }
    }

    res = requests.post(url, headers=headers, data=json.dumps(payload))
    data = res.json()
    resource_id = data['resourceId']
    sid = data['sid']
    server_response = data['serverResponse']
    mp4_link = server_response['fileList'][0]['fileName']
    m3u8_link = server_response['fileList'][1]['fileName']

    formatted_data = {'resource_id': resource_id, 'sid': sid,
                      'server_response': server_response, 'mp4_link': mp4_link, 'm3u8_link': m3u8_link}

    return formatted_data

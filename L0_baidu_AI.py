import requests
from playsound import playsound
import base64
import json
import urllib


def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    body = {
        "client_id": API_KEY,
        "client_secret": SECRET_KEY,
        "grant_type": "client_credentials"
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request(
        "POST",
        url, 
        headers=headers, 
        data=body
    )
    return response.json()['access_token']


API_KEY = 'syWLArnalaUQEGzh8YawpjMP'
SECRET_KEY = 'R6pjTuDkyO2t5RDwodvgo48L8cRY7HJM'
CUID = 'Br5NdKfjqMlwp6TJEgMDhp0qD3O5slzE'
ACCESS_TOKEN = get_access_token()


def get_file_content_as_base64(path, urlencoded=False):
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


def L0_Baidu_STT(audio_file):
    url = "https://vop.baidu.com/server_api"
    base64_audio = get_file_content_as_base64(audio_file)
    playsound(audio_file)
    body = json.dumps({
        "format": "m4a",
        "rate": 16000,
        "channel": 1,
        "cuid": CUID,
        "token": ACCESS_TOKEN,
        "speech": base64_audio,
        # "speech": audio_file,
        "len": 26496
    }, ensure_ascii=False)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=body.encode("utf-8")
    )
    print(response.text)
    # print(response.json()['result'][0])
    

def L0_Baidu_TTS(tex, filename="baidu_tts_output.mp3"):
    url = "https://tsn.baidu.com/text2audio"
    access_token = get_access_token()
    body = {
        'tex': tex,
        'tok': ACCESS_TOKEN,
        'cuid': CUID,
        'ctp': 1,
        'lan': 'zh',
        'spd': 7,
        'pit': 5,
        'vol': 5,
        'per': 110,
        'aue': 3
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*'
    }
    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=body
    )
    with open(filename, 'wb') as f:
        f.write(response.content)


if __name__ == '__main__':
    # L0_Baidu_TTS("您有新的美团外卖订单！请及时处理。")
    # L0_Baidu_TTS("滴滴司机您好，您的订单已经被接单，请尽快前往乘客位置。")
    # L0_Baidu_STT("./media/output.mp3")
    L0_Baidu_STT("./baidu_tts_output.mp3")
    # get_access_token()

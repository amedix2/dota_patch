import requests
import time
from config_dota_patch import Config


def send_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=data)
    return response.json()


def request_patch(ver):
    f = requests.get(url=f'https://www.dota2.com/datafeed/patchnotes?version={ver}')
    return f.json()['success']


token = Config.token
chat_id = Config.chat_id
text = Config.text

REQUIRED_VERSION = '7.34e'

i = 0

while True:
    try:
        r = request_patch(REQUIRED_VERSION)
        if r:
            send_message(token, chat_id, text)
            break
        else:
            print(f'{i}: waiting for the patch...')
            i += 10
        time.sleep(10)
    except Exception:
        print('exeption')
import requests
import time
from config_dota_patch import Config


def send_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=data)
    return response.json()


def request_patch(ver):
    try:
        f = requests.get(url=f'https://www.dota2.com/datafeed/patchnotes?version={ver}')
        return f.json()['success']
    except Exception:
        raise ConnectionAbortedError


token = Config.token
chat_id = Config.chat_id
text = Config.text

LINK = 'https://www.dota2.com/patches/'

REQUIRED_VERSION = Config.patch_version

i = 0

while True:
    try:
        r = request_patch(REQUIRED_VERSION)
        if r:
            send_message(token, chat_id, f'{text}\n{LINK + REQUIRED_VERSION}')
            break
        else:
            print(f'{i}: waiting for the patch {REQUIRED_VERSION}...')
            i += 10
    except ConnectionAbortedError:
        print('internet connection has been lost')
    except Exception as e:
        print(f'unknown error: {str(e)[:100]}')
    finally:
        time.sleep(10)

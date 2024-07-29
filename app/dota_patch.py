import requests
import time
import os
from dotenv import load_dotenv


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


if __name__ == '__main__':
    load_dotenv()
    LINK = 'https://www.dota2.com/patches/'
    token = os.getenv('TG_TOKEN')
    chat_id = int(os.getenv('TG_CHAT_ID'))
    text = os.getenv('MSG_TEXT')
    REQUIRED_VERSION = os.getenv('REQUIRED_VERSION')
    update_time = int(os.getenv('UPDATE_TIME'))

    i = 0
    while True:
        try:
            r = request_patch(REQUIRED_VERSION)
            if r:
                send_message(token, chat_id, f'{text}\n{LINK + REQUIRED_VERSION}')
                break
            else:
                print(f'{i}: waiting for the patch {REQUIRED_VERSION}...')
                i += update_time
        except ConnectionAbortedError:
            print('internet connection has been lost')
        except Exception as e:
            print(f'unknown error: {str(e)[:100]}')
        finally:
            time.sleep(update_time)

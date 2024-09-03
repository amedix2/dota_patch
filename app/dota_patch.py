import requests
import logging
import time
import os
from dotenv import load_dotenv

LINK = 'https://www.dota2.com/patches/'


def send_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=data)
    return response.json()


def request_patch():
    try:
        f = requests.get(url=f'https://www.dota2.com/datafeed/patchnoteslist').json()
        return f['patches'][-1]['patch_name']
    except Exception:
        raise ConnectionAbortedError


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    load_dotenv()
    token = os.getenv('TG_TOKEN')
    chat_id = int(os.getenv('TG_CHAT_ID'))
    text = os.getenv('MSG_TEXT')
    update_time = int(os.getenv('UPDATE_TIME'))

    current_patch = request_patch()
    logging.info(current_patch)

    i = 0
    while True:
        try:
            r = request_patch()
            if r != current_patch:
                send_message(token, chat_id, f'{text}\n{LINK + r}')
                break
            else:
                logging.info(f'{i}: current patch version - {r}')
                i += update_time
        except ConnectionAbortedError:
            logging.error('internet connection has been lost')
        except Exception as e:
            logging.error(f'unknown error: {str(e)[:100]}')
        finally:
            time.sleep(update_time)

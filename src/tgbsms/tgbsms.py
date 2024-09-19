import logging

import requests
from environs import Env

env = Env(eager=False)
env.read_env()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tgbsms")

ERROR_MSG = """
Missing telegram_chat_id/telegram_api_key. 
Pass it to the function or set as an environment variable TELEGRAM_CHAT_ID/TELEGRAM_API_KEY
"""


def send_message(text: str, telegram_chat_id: str | int | None = None, telegram_api_key: str | None = None) -> None:
    # Get the API key from environment variables if it's not passed directly
    telegram_api_key = telegram_api_key or env.str("TELEGRAM_API_KEY")
    telegram_chat_id = telegram_chat_id or env.str("TELEGRAM_CHAT_ID")

    if telegram_api_key is None or telegram_chat_id is None:
        raise SystemExit(ERROR_MSG)

    cropped_text = text[:4000]
    url = f"https://api.telegram.org/bot{telegram_api_key}/sendMessage"
    data = {"chat_id": telegram_chat_id, "text": cropped_text}

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        logger.info(f"Message sent successfully ({response.status_code})")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending message: {e}")
        logger.error(response.json())

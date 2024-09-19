import logging

import requests
from environs import Env

env = Env(eager=False)
env.read_env()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tgbsms")

ERROR_MSG = """
Missing telegram_chat_id/telegram_bot_token. 
Pass it to the function or set as an environment variable TELEGRAM_CHAT_ID/TELEGRAM_BOT_TOKEN
"""


def send_message(text: str, telegram_chat_id: str | int | None = None, telegram_bot_token: str | None = None) -> None:
    # Get the TOKEN from environment variables if it's not passed directly
    telegram_bot_token = telegram_bot_token or env.str("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = telegram_chat_id or env.str("TELEGRAM_CHAT_ID")

    if telegram_bot_token is None or telegram_chat_id is None:
        raise SystemExit(ERROR_MSG)

    cropped_text = text[:4000]
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    data = {"chat_id": telegram_chat_id, "text": cropped_text}

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        logger.info(f"Message sent successfully ({response.status_code})")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending message: {e}")
        logger.error(response.json())

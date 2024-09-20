import logging
from io import BytesIO

import requests
from environs import Env

from tgbsms.enums import ParseMode
from tgbsms.exceptions import EmptyPayloadError
from tgbsms.exceptions import NoTokenError
from tgbsms.exceptions import WrongParseModeError

env = Env(eager=False)
env.read_env()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tgbsms")

ENV_ERROR_MSG = """
Missing telegram_chat_id/telegram_bot_token. 
Pass it to the function or set as an environment variable TELEGRAM_CHAT_ID/TELEGRAM_BOT_TOKEN
"""

NO_DATA_ERROR_MSG = "Payload is empty"


def send_message(
    text: str = "",
    image: BytesIO | None = None,
    parse_mode: ParseMode = "HTML",
    telegram_chat_id: str | int | None = None,
    telegram_bot_token: str | None = None,
) -> None:
    # Get the TOKEN from environment variables if it's not passed directly
    telegram_bot_token = telegram_bot_token or env.str("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = telegram_chat_id or env.str("TELEGRAM_CHAT_ID")

    # No credentials check
    if telegram_bot_token is None or telegram_chat_id is None:
        raise NoTokenError(ENV_ERROR_MSG)

    # No data check
    if not any([text, image]):
        raise EmptyPayloadError(NO_DATA_ERROR_MSG)

    # Wrong parse_mode check
    if parse_mode not in ["HTML", "Markdown", "MarkdownV2"]:
        raise WrongParseModeError

    method = "sendMessage" if image is None else "sendPhoto"
    kword = "caption" if image else "text"
    url = f"https://api.telegram.org/bot{telegram_bot_token}/{method}"

    cropped_text = text[:4000]
    data = {"chat_id": telegram_chat_id, kword: cropped_text, "parse_mode": parse_mode}

    files = None
    if image:
        files = {"photo": image}

    try:
        response = requests.post(url, data, files=files)
        response.raise_for_status()
        logger.info(f"Message sent successfully ({response.status_code})")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending message: {e}")
        logger.error(response.json())

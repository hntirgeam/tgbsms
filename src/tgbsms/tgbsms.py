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

logger = logging.getLogger("tgbsms")

ENV_ERROR_MSG = """
Missing telegram_chat_id/telegram_bot_token. 
Pass it to the function or set as an environment variable TELEGRAM_CHAT_ID/TELEGRAM_BOT_TOKEN
"""

NO_DATA_ERROR_MSG = "Payload is empty"


def send_message(
    text: str = "",
    image: BytesIO | str | None = None,
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
    if parse_mode not in [pm for pm in ParseMode]:
        raise WrongParseModeError

    method = "sendMessage" if image is None else "sendPhoto"
    kword = "caption" if image else "text"
    url = f"https://api.telegram.org/bot{telegram_bot_token}/{method}"

    cropped_text = text[:4000]
    data = {"chat_id": telegram_chat_id, kword: cropped_text, "parse_mode": parse_mode.value}

    files = None
    if image:
        _data = {"photo": image}
        if isinstance(image, str):
            data.update(_data)
        else:
            files = _data

    try:
        response = requests.post(url, data, files=files)
        response.raise_for_status()
        
        result = response.json().get("result")
        msg_id = None
        if result:
            msg_id = result.get("message_id")
            
        logger.info(f"Message sent successfully (id: {msg_id})")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending message: {e}")
        logger.error(response.json())

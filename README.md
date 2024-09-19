# tgbsms - Telegram Bot Short Message Service

**tgbsms** is a simple Python utility for sending short messages via Telegram using the Telegram Bot API.


## Features

- Trims the text to fit Telegram's maximum length
- Sends text/images with Markdwon
- HTML/Markdown/MarkdownV2 parse_modes

## Installation

You can install **tgbsms** directly from PyPI using pip:

```bash
pip install tgbsms
```

## Usage

To send a message using the **tgbsms**, you can use the `send_message` function. Here is an example:

```python
from tgbsms import send_message

# Send text
send_message("message", telegram_chat_id="<chat_id>", telegram_bot_token="<your_bot_token>")
# Send image with text
send_message("message", telegram_chat_id="<chat_id>", telegram_bot_token="<your_bot_token>", image=open("image.png", "rb"))
# Send text with Markdown
send_message("__message__", telegram_chat_id="<chat_id>", telegram_bot_token="<your_bot_token>", parse_mode=ParseMode.MarkdownV2)
# Send text with Markdown and image
send_message("__message__", telegram_chat_id="<chat_id>", telegram_bot_token="<your_bot_token>", parse_mode=ParseMode.MarkdownV2, image=open("image.png", "rb"))
```

### Parameters:

- **`text`**: The message to send (string). If the message exceeds 4000 characters, it will be cropped.
- **`image`**: BytestIO object,
- **`parse_mode`**: ParseMode.HTML/Markdown/MarkdownV2 (`from enums import ParseMode`),
- **`telegram_chat_id`**: (Optional) The ID of the chat where the message will be sent. This can be an integer or a string.
- **`telegram_bot_token`**: (Optional) Your bot's TOKEN provided by Telegram.x

## Environment Variables

If you prefer not to pass the `telegram_bot_token` and `telegram_chat_id` directly, you can set them as environment variables:

- **`TELEGRAM_BOT_TOKEN`**: Your Telegram bot's TOKEN.
- **`TELEGRAM_CHAT_ID`**: The chat ID for the message.

Once the environment variables are set, the function can be used without passing these parameters directly.

```bash
export TELEGRAM_BOT_TOKEN="<your_bot_token>"
export TELEGRAM_CHAT_ID="<chat_id>"
```

And then:

```python
from tgbsms import send_message

send_message("test")
```

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/hntirgeam/tgbsms/blob/master/LICENSE) file for details.
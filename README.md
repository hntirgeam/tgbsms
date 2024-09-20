# tgbsms - Telegram Bot Short Message Service

**tgbsms** is a simple Python utility for sending short messages and/or images via Telegram using the Telegram Bot API.

## Features

- Automatically trims text to fit Telegram's maximum length
- Supports sending text and images
- Compatible with HTML, Markdown, and MarkdownV2 parse modes

## Installation

You can install **tgbsms** directly from PyPI using `pip`:

```bash
pip install tgbsms
```

## Usage

To send a message using **tgbsms**, you can use the `send_message` function. Here's an example:

```python3
from tgbsms import send_message

send_message(
    text="__message__",
    image=open("image.png", "rb"),
    parse_mode=ParseMode.MarkdownV2,
    telegram_chat_id="<chat_id>",
    telegram_bot_token="<your_bot_token>",
)
```

### Parameters

| Parameter              | Description                                                                               | Optional                                                   |
| ---------------------- | ----------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **text**               | The message to send (string). If the message exceeds 4000 characters, it will be cropped. | Yes. If there is an image passed to function               |
| **image**              | `file-like` or `BytesIO` object representing the image to send (optional).                | Yes. If there is a text passed to function                 |
| **parse_mode**         | One of `ParseMode.HTML`, `ParseMode.Markdown`, or `ParseMode.MarkdownV2` (from `enums`)   | Yes. Defaults to `HTML`                                    |
| **telegram_bot_token** | Your bot's token provided by [BotFather](https://t.me/BotFather).                         | Yes. If you export environment variable TELEGRAM_BOT_TOKEN |
| **telegram_chat_id**   | The chat ID where the message will be sent. Can be an integer or string.                  | Yes. If you export environment variable TELEGRAM_CHAT_ID   |

## Environment Variables

If you prefer not to pass the `telegram_bot_token` and `telegram_chat_id` directly, you can set them as environment variables:

- **`TELEGRAM_BOT_TOKEN`**: Your Telegram bot's token.
- **`TELEGRAM_CHAT_ID`**: The chat ID for the message.

Once the environment variables are set, the function can be used without passing these parameters directly

```bash
export TELEGRAM_BOT_TOKEN="<your_bot_token>"
export TELEGRAM_CHAT_ID="<chat_id>"
```

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/hntirgeam/tgbsms/blob/master/LICENSE) file for details.

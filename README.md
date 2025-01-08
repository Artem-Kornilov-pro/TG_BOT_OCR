# Telegram Bot for OCR with Yandex cloud

This project is a Telegram bot that uses Yandex Cloud OCR API to recognize text from images sent by users.

## Features

- Automatically retrieves and refreshes Yandex IAM tokens.
- Converts images to Base64 format for processing.
- Sends recognized text back to the user.

## Requirements

- Python 3.7+
- Telegram Bot Token
- Yandex Cloud OAuth Token
- Yandex Cloud Folder ID

## Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables**
   Create a `.env` file or set the following environment variables:
   ```bash
   export API_TOKEN_BOT=<your-telegram-bot-token>
   export OAUTH_TOKEN=<your-yandex-cloud-oauth-token>
   export FOLDER_ID=<your-yandex-folder-id>
   ```

4. **Run the Bot**
   ```bash
   python bot.py
   ```

## How It Works

1. The bot listens for incoming photo messages from users.
2. Upon receiving an image, it:
   - Downloads the image.
   - Encodes it in Base64 format.
   - Sends the encoded image to Yandex Cloud OCR API for text recognition.
3. The recognized text is sent back to the user.

## Files

- **bot.py**: Main script containing bot logic and Yandex OCR integration.
- **requirements.txt**: Python dependencies.

## Dependencies

- `telebot`
- `requests`
- `Pillow`

Install all dependencies using:
```bash
pip install -r requirements.txt
```

## Environment Variables

| Variable        | Description                                   |
|-----------------|-----------------------------------------------|
| `API_TOKEN_BOT` | Telegram bot API token                       |
| `OAUTH_TOKEN`   | Yandex Cloud OAuth token                     |
| `FOLDER_ID`     | Yandex Cloud folder ID                       |

## Notes

- Ensure your Yandex IAM token is refreshed every 11 hours (handled automatically by the script).
- Supported image format for OCR: JPEG.

## Troubleshooting

1. **Invalid IAM Token**
   - Ensure your `OAUTH_TOKEN` is valid and has sufficient permissions.

2. **Text Recognition Issues**
   - Ensure the image is clear and in JPEG format.

3. **Bot Fails to Start**
   - Check if the required environment variables are set.
   - Verify that all dependencies are installed.

## License

This project is licensed under the MIT License.


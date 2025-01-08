import telebot
import base64
import requests
import json
from PIL import Image
from io import BytesIO
import threading
import os
# Конфигурация
#API_TOKEN_BOT = '7605936873:AAEExBBpW45ZzBI39S46neFpYAIs2MReC7M' 
OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")
FOLDER_ID = os.getenv("FOLDER_ID")
API_TOKEN_BOT = os.getenv("API_TOKEN_BOT")
bot = telebot.TeleBot(API_TOKEN_BOT)
IAM_TOKEN = None

# Функция получения нового IAM токена
def get_new_iam_token():
    global IAM_TOKEN
    url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "yandexPassportOauthToken": OAUTH_TOKEN
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        IAM_TOKEN = response.json().get("iamToken")
        print("Получен новый IAM токен.")
    except Exception as e:
        print(f"Ошибка при получении IAM токена: {e}")

# Планировщик для обновления токена каждые 11 часов
def schedule_token_refresh():
    get_new_iam_token()
    threading.Timer(39600, schedule_token_refresh).start()  # 11 часов = 39600 секунд

# Функция кодирования изображения в Base64
def encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

# Функция распознавания текста через Yandex OCR API
def recognize_text(image_base64):
    url = "https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {IAM_TOKEN}",
        "x-folder-id": FOLDER_ID
    }
    body = {
        "mimeType": "JPEG",
        "languageCodes": ["*"],
        "content": image_base64
    }
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        print("Ответ сервера:", response.text)
        return response.json()
    except Exception as e:
        print(f"Ошибка при запросе к Yandex OCR API: {e}")
        return {}

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # Получаем файл изображения
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Конвертируем в base64
        with Image.open(BytesIO(downloaded_file)) as img:
            image_base64 = encode_image(img)

        # Распознаём текст
        result = recognize_text(image_base64)

        # Проверяем, есть ли текст в ответе
        if "result" in result and "textAnnotation" in result["result"] and "fullText" in result["result"]["textAnnotation"]:
            recognized_text = result["result"]["textAnnotation"]["fullText"]
            bot.reply_to(message, recognized_text or "Текст не распознан.")
        else:
            bot.reply_to(message, "Не удалось распознать текст.")
    except Exception as e:
        print(f"Ошибка обработки сообщения: {e}")
        bot.reply_to(message, "Произошла ошибка при обработке изображения.")

# Запускаем обновление IAM токена и бота
schedule_token_refresh()
bot.polling(none_stop=True)
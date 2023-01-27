from os import path
from pathlib import Path
from urllib.parse import unquote, urlsplit
import requests
import telegram


def publish_image_to_channel(filepath, tg_bot_token, tg_channel_id):
    bot = telegram.Bot(token=tg_bot_token)
    with open(filepath, 'rb') as photo:
        bot.send_photo(
            chat_id=tg_channel_id,
            photo=photo,
            timeout=20.)


def get_extension(url):
    file_path = unquote(urlsplit(url).path)
    _, extension = path.splitext(file_path)
    return extension


def upload_image(image_url, image_name, image_folder, params=None):
    Path(image_folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(image_url, params=params)
    response.raise_for_status()
    with open(image_name, 'wb') as file:
        file.write(response.content)



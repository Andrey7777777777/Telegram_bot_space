from os import path
from datetime import datetime
import requests
from environs import Env
from image_downloading import upload_image


def fetch_epic_nasa_image(image_folder, nasa_api_key):
    params = {'api_key': nasa_api_key}
    epic_images_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    response = requests.get(epic_images_url, params=params)
    response.raise_for_status()
    response_payload = response.json()
    for image in response_payload:
        file_image_name, epic_image_url = epic_image_name_and_url(image)
        try:
            upload_image(epic_image_url, path.join(image_folder, file_image_name), params)
            print(epic_image_url, 'Загружена')
        except requests.exceptions.HTTPError:
            print('Ошибка! Не удалось загрузить фотографию:', epic_image_url)


def epic_image_name_and_url(image):
    file_extension = '.png'
    image_date, _ = image['date'].split()
    image_date = datetime.fromisoformat(image_date).date()
    image_name = image['image']
    image_name = f'{image_name}{file_extension}'
    image_url = f'https://api.nasa.gov/EPIC/archive/natural/{image_date.year}/{image_date.month:02d}/{image_date.day:02d}/png/{image_name}'
    return image_name, image_url


def main():
    env = Env()
    env.read_env()
    image_folder = env.str('IMAGE_FOLDER', default='images')
    nasa_api_key = env.str('NASA_API_KEY', default='DEMO_KEY')
    fetch_epic_nasa_image(image_folder, nasa_api_key)


if __name__ == '__main__':
    main()
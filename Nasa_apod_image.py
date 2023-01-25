import argparse
from os import path
import requests
from environs import Env
from image_downloading import upload_image, get_extension


def input_parsing_command_line():
    parser = argparse.ArgumentParser(
        description='Программа скачивает фотографии космоса Nasa'
    )
    parser.add_argument(
        '--count',
        help='Количество фото',
        default='5'
    )
    args = parser.parse_args()
    return args


def fetch_nasa_image_apod(image_folder, nasa_api_key, images_quantity):
    nasa_apod_image_url = 'https://api.nasa.gov/planetary/apod'
    params = {'count': images_quantity, 'api_key': nasa_api_key}
    response = requests.get(nasa_apod_image_url, params=params)
    response.raise_for_status()
    random_apods = response.json()
    for num, apod in enumerate(random_apods, 1):
        try:
            image_url = apod['hdurl']
        except KeyError:
            print('Не удалось получить ссылку на фотографию.')
            print(apod)
            continue
        file_extension = get_extension(image_url)
        image_name = f'nasa{num}{file_extension}'
        try:
            upload_image(image_url, path.join(image_folder, image_name))
            print(image_url, 'Загружена')
        except requests.exceptions.HTTPError:
            print('Ошибка! Не удалось загрузить фотографию:', image_url)


def main():
    env = Env()
    env.read_env()
    image_folder = env.str('IMAGE_FOLDER', default='images')
    nasa_api_key = env.str('NASA_API_KEY', default='DEMO_KEY')
    images_quantity = input_parsing_command_line().count
    fetch_nasa_image_apod(image_folder, nasa_api_key, images_quantity)


if __name__ == '__main__':
    main()
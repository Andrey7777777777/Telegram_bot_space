import requests
import argparse
from os import path
from environs import Env
from image_downloading import upload_image, get_extension


def input_parsing_command_line():
    parser = argparse.ArgumentParser(
        description='Программа скачивает фотографии запуска SpaceX'
    )
    parser.add_argument('-id', help='Введите id запуска', default='latest')
    args = parser.parse_args()
    return args


def fetch_spacex_last_launch(space_id):
    env = Env()
    env.read_env()
    image_folder = env.str('IMAGE_FOLDER', default='images')
    spacex_url = f'https://api.spacexdata.com/v5/launches/{space_id}'
    params = {}
    response = requests.get(spacex_url, params=params)
    response.raise_for_status()
    response_data = response.json()['links']['flickr']['original']
    for url_number, url in enumerate(response_data):
        file_name = 'spacex{}{}'.format(
            url_number,
            get_extension(url)
        )
        upload_image(url, path.join(image_folder, file_name))


if __name__ == '__main__':
    space_id = input_parsing_command_line().id
    fetch_spacex_last_launch(space_id)



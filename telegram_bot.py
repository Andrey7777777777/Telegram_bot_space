import os
import argparse
from random import choice
from environs import Env
from image_downloading import publish_image_to_channel


def main():
    parser = argparse.ArgumentParser(
        description='''Скрипт публикует изображение в телеграм-канал Foto_space'''
    )
    parser.add_argument(
        '--name',
        help='''Введите название изображения, которое необходимо опубликовать 
                или не вводите ничего для публикации случайного изображения''')
    args = parser.parse_args()
    files_in_dir = os.listdir('images')
    path_to_dir = os.path.join(os.getcwd(), 'images')
    if args.name in files_in_dir:
        path_to_file = os.path.join(path_to_dir, args.name)
    else:
        file_name = choice(files_in_dir)
        path_to_file = os.path.join(path_to_dir, file_name)
    publish_image_to_channel(path_to_file, tg_bot_token, tg_channel_id)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    tg_bot_token = env.str('TG_BOT_TOKEN')
    tg_channel_id = env.str('TG_CHANNEL_ID')
    main()
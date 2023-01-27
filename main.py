import time
import os
import telegram
from environs import Env
import argparse
from random import shuffle
from pathlib import Path
from image_downloading import publish_image_to_channel


def main():
    env = Env()
    env.read_env()
    image_folder = env.str('IMAGE_FOLDER', default='images')
    Path(image_folder).mkdir(parents=True, exist_ok=True)
    tg_bot_token = env.str('TG_BOT_TOKEN')
    tg_channel_id = env.str('TG_CHANNEL_ID')
    parser = argparse.ArgumentParser(
        description='''Скрипт автоматически публикует изображения в 
                           телеграм-канал "КосмоФото" с заданным интервалом''')
    parser.add_argument('--interval',
                        help='''
                        Введите необходимый интервал (целое число) 
                        для публикации изображений илипропустите команду
                        (интервал публикаций по умолчанию - 4 часа)
                                ''',
                        default=4,
                        type=int
                        )
    args = parser.parse_args()
    filenames = os.listdir('images')
    directorypath = os.path.join(os.getcwd(), 'images')
    while True:
        shuffle(filenames)
        for filename in filenames:
            filepath = os.path.join(directorypath, filename)
            try:
                publish_image_to_channel(filepath, tg_bot_token, tg_channel_id)
            except telegram.error.NetworkError:
                print('Неудачная попытка соединения')
            time.sleep(args.interval * 3600)


if __name__ == '__main__':
    main()







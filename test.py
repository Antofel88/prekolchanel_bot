import telebot
import schedule
import time
import os
import random
import yadisk
import logging
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO)


load_dotenv()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
y = yadisk.YaDisk(token=os.getenv("YA_TOKEN"))

ya_disk_folder_video = "prekolchanel_video"  # папка яндекс диска с видосами


# формируем список файлов папки яндекс диска
def creation_yandex_list(folder):
    yandex_list = [i["name"] for i in y.listdir(folder)]
    return yandex_list


# выбор случайного видео, скачивание, постинг и удаление
def send_precol_video(folder):
    precol_list = creation_yandex_list(folder)
    if precol_list:
        # выбираем случайное видео
        precol = random.choice(precol_list)
        # скачиваем видео
        y.download(
            f"{folder}/{precol}",
            f"videos/{precol}",
        )
        # указываем путь для скачанного видео
        video_path = os.path.join(
            "videos",
            precol,
        )
        # открываем видео и отправляем в чат
        with open(video_path, "rb") as video:
            bot.send_video(chat_id=os.getenv("chat_id_public_test"), video=video)

        # удаляем с Яндекс.Диска и локально
        y.remove(f"{folder}/{precol}")
        os.remove(f"videos/{precol}")

    else:
        bot.send_message(
            chat_id=os.getenv("chat_id_admin"), text="СЭР, Видео-приколы закончились!"
        )


send_precol_video(ya_disk_folder_video)

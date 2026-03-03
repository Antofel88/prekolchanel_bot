import telebot
import sqlite3
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

ya_disk_folder_images = "prekolchanel_images"  # папка яндекс диска с картинками
ya_disk_folder_videos = "prekolchanel_videos"  # папка яндекс диска с видосами


# Формируем список файлов папки яндекс диска
def creation_yandex_list(folder):
    yandex_list = [i["name"] for i in y.listdir(folder)]
    return yandex_list


# выбор случайной картинки и афоризма, скачивание, постинг и удаление
def send_prekol_image(folder):

    prekol_list = creation_yandex_list(folder)

    if prekol_list:
        # выбираем случайную картинку
        prekol_name = random.choice(prekol_list)
        # скачиваем картинку
        y.download(
            f"{folder}/{prekol_name}",
            f"images/{prekol_name}",
        )
        # указываем путь для скачанной картинки
        photo_path = os.path.join(
            "images",
            prekol_name,
        )

        # открываем картинку, добавляем афоризм и отправляем в чат
        with open(photo_path, "rb") as photo:
            bot.send_photo(chat_id=os.getenv("chat_id_public_test"), photo=photo)

        # удаляем с Яндекс.Диска и локально
        y.remove(f"{folder}/{prekol_name}")
        os.remove(f"images/{prekol_name}")

    else:
        bot.send_message(
            chat_id=os.getenv("chat_id_admin"), text="Картинки закончились!"
        )


# выбор случайного видео, скачивание, постинг и удаление
def send_prekol_video(folder):
    prekol_list = creation_yandex_list(folder)
    if prekol_list:
        # выбираем случайное видео
        prekol_name = random.choice(prekol_list)
        # скачиваем видео
        y.download(
            f"{folder}/{prekol_name}",
            f"videos/{prekol_name}",
        )
        # указываем путь для скачанного видео
        video_path = os.path.join(
            "videos",
            prekol_name,
        )

        # открываем видео и отправляем в чат
        with open(video_path, "rb") as video:
            bot.send_video(chat_id=os.getenv("chat_id_public_test"), video=video)

        # удаляем с Яндекс.Диска и локально
        y.remove(f"{folder}/{prekol_name}")
        os.remove(f"videos/{prekol_name}")

    else:
        send_prekol_image(ya_disk_folder_images)


# отправка количества оставшихся мемов в папке яндекс диска админу
def send_prekol_amount():

    number_of_images = len(creation_yandex_list(ya_disk_folder_images))
    number_of_videos = len(creation_yandex_list(ya_disk_folder_videos))

    bot.send_message(
        chat_id=os.getenv("chat_id_admin"),
        text=f"Остатки картинок: {number_of_images}\nОстатки видосов: {number_of_videos}",
    )


send_prekol_image(ya_disk_folder_images)

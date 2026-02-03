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

ya_disk_folder = "prekolchanel_image"  # папка яндекс диска с картинками
ya_disk_folder_video = "prekolchanel_video"  # папка яндекс диска с видосами


# Формируем список файлов папки яндекс диска
def creation_yandex_list(folder):
    yandex_list = [i["name"] for i in y.listdir(folder)]
    return yandex_list


print(creation_yandex_list(ya_disk_folder))

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

ya_disk_folder = "prekolchanel"  # папка яндекс диска
ya_disk_folder_video = "prekolchanel_video"  # папка яндекс диска с видосами


# формируем список файлов папки яндекс диска
def creation_yandex_list(folder):
    yandex_list = [i["name"] for i in y.listdir(folder)]
    return yandex_list


# выбор случайной дневной картинки, скачивание, постинг и удаление
def send_precol(folder):
    precol_list = creation_yandex_list(folder)
    if precol_list:
        # выбираем случайную картинку
        precol = random.choice(precol_list)
        # скачиваем картинку
        y.download(
            f"{folder}/{precol}",
            f"images/{precol}",
        )
        # указываем путь для скачанной картинки
        photo_path = os.path.join(
            "images",
            precol,
        )
        # открываем картинку и отправляем в чат
        with open(photo_path, "rb") as photo:
            bot.send_photo(chat_id=os.getenv("chat_id_public"), photo=photo)

        # удаляем с Яндекс.Диска и локально
        y.remove(f"{folder}/{precol}")
        os.remove(f"images/{precol}")

    else:
        bot.send_message(
            chat_id=os.getenv("chat_id_admin"), text="СЭР, Приколы закончились!"
        )


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
            bot.send_video(chat_id=os.getenv("chat_id_public"), video=video)

        # удаляем с Яндекс.Диска и локально
        y.remove(f"{folder}/{precol}")
        os.remove(f"videos/{precol}")

    else:
        send_precol(ya_disk_folder)


# отправка количества оставшихся мемов в папке яндекс диска админу
def send_amount_precol():
    bot.send_message(
        chat_id=os.getenv("chat_id_admin"),
        text=f"Остатки картинок: {len(creation_yandex_list(ya_disk_folder))}\nОстатки видосов: {len(creation_yandex_list(ya_disk_folder_video))}",
    )


schedule.every().day.at("06:00").do(send_precol, ya_disk_folder)
schedule.every().day.at("08:00").do(send_precol_video, ya_disk_folder_video)
schedule.every().day.at("10:00").do(send_precol, ya_disk_folder)
schedule.every().day.at("12:00").do(send_precol, ya_disk_folder)
schedule.every().day.at("15:00").do(send_precol, ya_disk_folder)
schedule.every().day.at("17:00").do(send_precol, ya_disk_folder)
schedule.every().day.at("19:00").do(send_precol_video, ya_disk_folder_video)
schedule.every().day.at("21:00").do(send_precol, ya_disk_folder)
schedule.every().day.at("21:02").do(send_amount_precol)

while True:
    schedule.run_pending()
    time.sleep(1)

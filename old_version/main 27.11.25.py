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
ya_disk_folder_first = "prekolchanel_first"  # папка яндекс диска с утренними мемами
ya_disk_folder_last = "prekolchanel_last"  # папка яндекс диска с вечерними мемами


# формируем список файлов папки яндекс диска
def creation_yandex_list(folder):
    yandex_list = [i["name"] for i in y.listdir(folder)]
    return yandex_list


# выбор утренней случайной картинки, скачивание, постинг и удаление
def send_precol_first(folder):
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

        y.remove(f"{folder}/{precol}")
        os.remove(f"images/{precol}")

    else:
        send_precol(ya_disk_folder)


# выбор вечерней случайной картинки, скачивание, постинг и удаление
def send_precol_last(folder):
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

        y.remove(f"{folder}/{precol}")
        os.remove(f"images/{precol}")

    else:
        send_precol(ya_disk_folder)


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

        y.remove(f"{folder}/{precol}")
        os.remove(f"images/{precol}")

    else:
        bot.send_message(
            chat_id=os.getenv("chat_id_admin"), text="СЭР, Приколы закончились!"
        )


# отправка количества оставшихся мемов в папке яндекс диска админу
def send_amount_precol():
    bot.send_message(
        chat_id=os.getenv("chat_id_admin"),
        text=f"Остатки мемов:\n\nУтренние: {len(creation_yandex_list(ya_disk_folder_first))}\nДневные: {len(creation_yandex_list(ya_disk_folder))}\nВечерние: {len(creation_yandex_list(ya_disk_folder_last))}",
    )


schedule.every().day.at("06:00").do(send_precol_first, ya_disk_folder_first)
schedule.every().day.at("08:00").do(send_precol, ya_disk_folder)
schedule.every().day.at("10:00").do(send_precol, ya_disk_folder)
schedule.every().day.at("12:00").do(send_precol, ya_disk_folder)
schedule.every().day.at("17:00").do(send_precol, ya_disk_folder)
schedule.every().day.at("21:00").do(send_precol_last, ya_disk_folder_last)
schedule.every().day.at("21:02").do(send_amount_precol)

while True:
    schedule.run_pending()
    time.sleep(1)

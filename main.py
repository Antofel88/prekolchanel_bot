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


# Получает список афоризмов из БД
def get_list_aphorisms():
    with sqlite3.connect("aphorisms.db") as conn:
        cursor = conn.cursor()

        # Получаем все афоризмы в виде списка
        cursor.execute("SELECT id, text FROM aphorisms")
        aphorisms = cursor.fetchall()

        return aphorisms


# Удаляет афоризм из БД
def remove_aphorism(aph_id):
    with sqlite3.connect("aphorisms.db") as conn:
        cursor = conn.cursor()

        cursor.execute("DELETE FROM aphorisms WHERE id = ?", (aph_id,))


# Получает случайный афоризм и удаляет его
def get_random_aphorism():

    aphorisms = get_list_aphorisms()

    if not aphorisms:
        bot.send_message(
            chat_id=os.getenv("chat_id_admin"), text="Бомбовые цитаты закончились!"
        )
        return ""

    # Выбираем случайный афоризм из списка, т.к. элемент списка это кортеж с двумя значениями, то присваиваем переменным id и сам текст
    aph_id, aph_text = random.choice(aphorisms)

    # Удаляем его с помошью отдельной функции
    remove_aphorism(
        aph_id,
    )

    # Возвращаем текст афоризма
    return aph_text


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
        # Получаем афоризм из фунции
        caption = get_random_aphorism()

        # открываем картинку, добавляем афоризм и отправляем в чат
        with open(photo_path, "rb") as photo:
            bot.send_photo(
                chat_id=os.getenv("chat_id_public"), caption=caption, photo=photo
            )
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
        # Получаем афоризм из фунции
        caption = get_random_aphorism()

        # открываем видео и отправляем в чат
        with open(video_path, "rb") as video:
            bot.send_video(
                chat_id=os.getenv("chat_id_public"), caption=caption, video=video
            )

        # удаляем с Яндекс.Диска и локально
        y.remove(f"{folder}/{prekol_name}")
        os.remove(f"videos/{prekol_name}")

    else:
        send_prekol_image(ya_disk_folder_images)


# отправка количества оставшихся мемов в папке яндекс диска админу
def send_prekol_amount():

    number_of_images = len(creation_yandex_list(ya_disk_folder_images))
    number_of_videos = len(creation_yandex_list(ya_disk_folder_videos))
    number_of_aphorisms = len(get_list_aphorisms())

    bot.send_message(
        chat_id=os.getenv("chat_id_admin"),
        text=f"Остатки картинок: {number_of_images}\nОстатки афоризмов: {number_of_aphorisms}\nОстатки видосов: {number_of_videos}",
    )


schedule.every().day.at("06:00").do(send_prekol_image, ya_disk_folder_images)
schedule.every().day.at("07:00").do(send_prekol_video, ya_disk_folder_videos)
schedule.every().day.at("09:00").do(send_prekol_image, ya_disk_folder_images)
schedule.every().day.at("11:00").do(send_prekol_image, ya_disk_folder_images)
schedule.every().day.at("13:00").do(send_prekol_image, ya_disk_folder_images)
schedule.every().day.at("15:00").do(send_prekol_image, ya_disk_folder_images)
schedule.every().day.at("17:00").do(send_prekol_image, ya_disk_folder_images)
schedule.every().day.at("18:00").do(send_prekol_image, ya_disk_folder_images)
schedule.every().day.at("19:00").do(send_prekol_video, ya_disk_folder_videos)
schedule.every().day.at("21:00").do(send_prekol_image, ya_disk_folder_images)
schedule.every().day.at("21:02").do(send_prekol_amount)

while True:
    schedule.run_pending()
    time.sleep(1)

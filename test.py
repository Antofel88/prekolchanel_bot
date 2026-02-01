import telebot
import schedule
import time
import os
import random
import yadisk
import logging
from dotenv import load_dotenv


import requests
from deep_translator import GoogleTranslator


logging.basicConfig(level=logging.INFO)

load_dotenv()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

url = "https://uselessfacts.jsph.pl/random.json?language=en"
response = requests.get(url)
data = response.json()
fact = data["text"]

fact_translated = GoogleTranslator(source="auto", target="ru").translate(fact)

caption = f"Интересный факт:\n\n{fact_translated}"


photo_path = os.path.join(
    "images",
    "photo_2025-12-29_11-54-26.jpg",
)

# открываем картинку и отправляем в чат
with open(photo_path, "rb") as photo:
    bot.send_photo(
        chat_id=os.getenv("chat_id_public_test"), photo=photo, caption=caption
    )

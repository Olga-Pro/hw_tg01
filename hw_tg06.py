import asyncio
from aiogram import Bot, Dispatcher, F

from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup


import keyb_tg06 as kb

import logging
import sqlite3
import requests
import random

import os

from dotenv import load_dotenv
# Загрузка переменных окружения из файла .env
load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# Создание экземпляра бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


# Создаем БД для хранения данных о пользователях и расходах
conn = sqlite3.connect('user.db')
cursor = conn.cursor()
cursor.execute(''' CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    telegram_id INTEGER UNIQUE,
    name TEXT,
    category1 TEXT,
    category2 TEXT,
    category3 TEXT,
    expenses1 REAL,
    expenses2 REAL,
    expenses3 REAL
    )
''')
conn.commit()

# Класс состояния для каждой категории и каждого значения
class FinancesForm(StatesGroup):
    category1 = State()
    expenses1 = State()
    category2 = State()
    expenses2 = State()
    category3 = State()
    expenses3 = State()

# Задание 1: Создание простого меню с кнопками
@dp.message(CommandStart())
async def send_welcome(message: Message):
    keyboards = kb.keyboards
    await message.answer("Привет! Я ваш личный финансовый помощник. Выберите опцию из меню:", reply_markup=keyboards)


@dp.message(F.text == "Регистрация в ТГ-боте")
async def registration(message: Message):
    telegram_id = message.from_user.id
    name = message.from_user.full_name
    cursor.execute('''SELECT * from users WHERE telegram_id = ?''', (telegram_id,))
    user = cursor.fetchone()
    if user:
        await message.answer("Вы уже зарегистрированы!")
    else:
        cursor.execute('''INSERT INTO users (telegram_id, name) VALUES (?, ?)''', (telegram_id, name))
        conn.commit()
        await message.answer("Вы успешно зарегистрированы!")


@dp.message(F.text == "Курс валют")
async def exchange_rates(message: Message):
    url ="https://v6.exchangerate-api.com/v6/09edf8b2bb246e1f801cbfba/latest/USD"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            await message.answer("Не удалось получить данные о курсе валют!")
            return
        usd_to_rub = data['conversion_rates']['RUB']
        eur_to_usd = data['conversion_rates']['EUR']

        eur_to_rub = eur_to_usd * usd_to_rub

        await message.answer(f"1 USD = {usd_to_rub:.2f}\n"
                             f"1 EUR = {eur_to_rub:.2f}  RUB")

    except:
        await message.answer("Произошла ошибка!")


@dp.message(F.text == "Советы по экономии")
async def send_tips(message: Message):
    tips = {
        "Совет 1: Ведите бюджет и следите за своими расходами.",
        "Совет 2: Откладывайте часть доходов на сбережения.",
        "Совет 3: Покупайте товары по скидкам и распродажам."
            }
    tip = random.choice(tips)
    await message.answer(tip)

# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

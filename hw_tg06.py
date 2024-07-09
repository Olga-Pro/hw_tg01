import asyncio
from aiogram import Bot, Dispatcher, F

from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage


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
conn = sqlite3.connect('users_tg06.db')
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
    tips = [
        "Совет 1: Ведите бюджет и следите за своими расходами.",
        "Совет 2: Откладывайте часть доходов на сбережения.",
        "Совет 3: Покупайте товары по скидкам и распродажам."
            ]
    tip = random.choice(tips)
    await message.answer(tip)


@dp.message(F.text == "Личные финансы")
async def finances(message: Message, state: FSMContext):
    await state.set_state(FinancesForm.category1)
    await message.reply("Введите первую категорию расходов")


@dp.message(FinancesForm.category1)
async def finances(message: Message, state: FSMContext):
    await state.update_data(category1 = message.text)
    await state.set_state(FinancesForm.expenses1)
    await message.reply("Введите расходы для категории 1:")


@dp.message(FinancesForm.expenses1)
async def finances(message: Message, state: FSMContext):
    await state.update_data(expenses1 = float(message.text))
    await state.set_state(FinancesForm.category2)
    await message.reply("Введите вторую категорию расходов:")

@dp.message(FinancesForm.category2)
async def finances(message: Message, state: FSMContext):
    await state.update_data(category2 = message.text)
    await state.set_state(FinancesForm.expenses2)
    await message.reply("Введите расходы для категории 2:")


@dp.message(FinancesForm.expenses2)
async def finances(message: Message, state: FSMContext):
    await state.update_data(expenses2 = float(message.text))
    await state.set_state(FinancesForm.category3)
    await message.reply("Введите третью категорию расходов:")

@dp.message(FinancesForm.category3)
async def finances(message: Message, state: FSMContext):
    await state.update_data(category3 = message.text)
    await state.set_state(FinancesForm.expenses3)
    await message.reply("Введите расходы для категории 3:")


@dp.message(FinancesForm.expenses3)
async def finances(message: Message, state: FSMContext):
    data = await state.get_data()
    telegram_id = message.from_user.id
    cursor.execute('''
    UPDATE users SET category1 = ?, expenses1 = ?, category2 = ?, expenses2 = ?, category3 = ?, expenses3 = ?
    WHERE telegram_id = ?''',
                   (data['category1'], data['expenses1'],data['category2'], data['expenses2'],
                    data['category3'], float(message.text),telegram_id)
                   )
    conn.commit()
    await state.clear()

    await message.answer("Категории и расходы сохранены!")


@dp.message(Command(commands=['base']))
async def show_base(message: Message):
    # Извлечение всех данных из базы данных
    conn = sqlite3.connect('users_tg06.db')
    cur = conn.cursor()
    cur.execute('''SELECT id, telegram_id, name,  
                category1, category2, category3, 
                expenses1, expenses2, expenses3 FROM users''')
    rows = cur.fetchall()
    conn.close()

    # Формирование сообщения с данными
    if rows:
        response = "Содержимое таблицы БД:\n\n"
        for row in rows:
            response += f"ID: {row[0]}, TG ID: {row[1]}, Имя: {row[2]}\n"
            response += f"{row[3]} - {row[6]}\n"
            response += f"{row[4]} - {row[7]}\n"
            response += f"{row[5]} - {row[8]}\n\n"
    else:
        response = "В базе данных нет данных."

    # Отправка сообщения пользователю
    await message.answer(response)
# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

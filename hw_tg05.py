import asyncio
from aiogram import Bot, Dispatcher, F

from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

import requests

from googletrans import Translator

import keyb_tg05 as kb

import os

from dotenv import load_dotenv
# Загрузка переменных окружения из файла .env
load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# Создание экземпляра бота
bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()


def get_random_math_fact():
    url = 'http://numbersapi.com/random/math'
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return 'Не удалось получить данные от NumbersAPI.'


async def send_math_fact(message: Message):
    mfact = math_fact()
    try:
        translated = translator.translate(mfact, src='auto', dest='ru')
        await message.answer(translated.text)
    except Exception as e:
        await message.answer(f"Error: {e}")
        print(f"Ошибка при переводе: {mfact} - {e}")


def math_fact():
    fact = get_random_math_fact()
    return fact


@dp.message(CommandStart())
async def send_welcome(message: Message):
    # keyboard = kb.inline_keyboard  # Для варианта с инлайн-кнопкой
    keyboard = kb.keyboard1
    await message.answer("Нажми кнопку или введи /math для получения случайного математического факта",
                         reply_markup=keyboard)


@dp.message(Command("math"))
async def math_command(message: Message):
   await send_math_fact(message)


@dp.message(F.text == "Случайный математический факт")
async def math_button(message: Message):
    await send_math_fact(message)


# Инлайн-кнопка: нет эхо-запроса в чат, но неудобно для многократного нажатия
# @dp.callback_query(F.data == "math_fact")
# async def math_button(callback_query: CallbackQuery):
#     await send_math_fact(callback_query.message)
#     await callback_query.answer()


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

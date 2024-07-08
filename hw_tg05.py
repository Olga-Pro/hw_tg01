import asyncio
from aiogram import Bot, Dispatcher, F

from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
#from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import keyb_tg05 as kb

import os

from dotenv import load_dotenv
# Загрузка переменных окружения из файла .env
load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# Создание экземпляра бота
bot = Bot(token=TOKEN)
dp = Dispatcher()


# Задание 1: Создание простого меню с кнопками
@dp.message(CommandStart())
async def send_welcome(message: Message):
    keyboard = kb.keyboard2
    await message.answer("Выберите опцию:", reply_markup=keyboard)




# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

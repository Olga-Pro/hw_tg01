import asyncio
from aiogram import Bot, Dispatcher, F

from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
#from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import keyb_tg04 as kb

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

@dp.message(lambda message: message.text in ["Привет", "Пока"])
async def handle_menu(message: Message):
    if message.text == "Привет":
        await message.reply(f"Привет, {message.from_user.first_name}!")
    elif message.text == "Пока":
        await message.reply(f"До свидания, {message.from_user.first_name}!")

@dp.message(Command(commands=['links']))
async def show_links(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!", reply_markup=kb.inline_keyboard1)


@dp.message(Command(commands=['dinamic']))
async def dinamic(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!", reply_markup=kb.inline_keyboard2)

@dp.callback_query(F.data == 'dinamic')
async def new_buttons(callback: CallbackQuery):
   await callback.message.edit_text('Вот другие кнопки!', reply_markup=await kb.new_keyboard1())

# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


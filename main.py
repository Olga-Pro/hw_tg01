import os

import asyncio
from aiogram import Bot, Dispatcher

from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import aiohttp

from dotenv import load_dotenv
# Загрузка переменных окружения из файла .env
load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEATHER_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
CITY = 'Москва'

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def get_weather(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                main_ = data['main']
                weather = data['weather'][0]
                temp = main_['temp']
                description = weather['description']
                return f"Сейчас в городе {city} {temp} °C\nПогода: {description.capitalize()}"
            else:
                return "Извините, данные о погоде недоступны"


@dp.message(Command(commands=['help']))
async def help_mess(message: Message):
    await message.answer('Этот бот умеет выполнять команды:\n/start\n/help\n/weather')


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я - бот!")


@dp.message(Command(commands=['weather']))
async def send_weather(message: Message):
    weather_info = await get_weather(CITY, WEATHER_API_KEY)
    await message.reply(weather_info)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

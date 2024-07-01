import asyncio
from aiogram import Bot, Dispatcher

from aiogram import types
from aiogram.types import InputFile
from googletrans import Translator
from gtts import gTTS


import os

from dotenv import load_dotenv
# Загрузка переменных окружения из файла .env
load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# Создание экземпляра бота
bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()

# Создаем папку для изображений, если она не существует
if not os.path.exists('img'):
    os.makedirs('img')

@dp.message(content_types=['photo'])
async def handle_photos(message: types.Message):
    photo = message.photo[-1]  # Берем самое большое разрешение фото
    photo_id = photo.file_id
    file = await bot.get_file(photo_id)
    file_path = file.file_path
    destination = f'img/{photo_id}.jpg'
    await bot.download_file(file_path, destination)
    await message.reply("Фото сохранено!")

@dp.message(commands=['voice'])
async def send_voice(message: types.Message):
    tts = gTTS("Hello, this is a voice message from your bot", lang='en')
    tts.save("voice.mp3")
    voice = InputFile("voice.mp3")
    await bot.send_voice(message.chat.id, voice)
    os.remove("voice.mp3")

@dp.message(content_types=['text'])
async def translate_text(message: types.Message):
    translated = translator.translate(message.text, src='auto', dest='en')
    await message.reply(translated.text)

# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

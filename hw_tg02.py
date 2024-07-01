import asyncio
from aiogram import Bot, Dispatcher

from aiogram import types
from aiogram.types import Message, FSInputFile
from gtts import gTTS

from aiogram.filters import CommandStart, Command
from googletrans import Translator


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


@dp.message(Command(commands=['help']))
async def help_mess(message: Message):
    await message.answer('Этот бот умеет выполнять команды:\n/start\n/photo\n/voice\n/text\n/help')


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я - бот!")

@dp.message(Command(commands=['photo']))
async def request_photo(message: Message):
    await message.answer("Пожалуйста, отправьте мне фото")
@dp.message((lambda message: 'photo' in message.content_type))
async def handle_photos(message: Message):
    photo = message.photo[-1]  # Берем самое большое разрешение фото
    photo_id = photo.file_id
    file = await bot.get_file(photo_id)
    file_path = file.file_path
    destination = f'img/{photo_id}.jpg'
    await bot.download_file(file_path, destination)
    await message.reply("Фото сохранено!")

@dp.message(Command(commands='voice'))
async def send_voice(message: types.Message):
    tts = gTTS("Привет, это голосовое сообщение от вашего бота", lang='ru')

    file_path = "voice1.ogg"

    # Сохранение файла
    tts.save(file_path)

    # Отправка файла
    voice = FSInputFile(file_path)
    await bot.send_voice(message.chat.id, voice)

    # Удаление файла
    os.remove(file_path)

@dp.message(Command(commands=['text']))
async def request_photo(message: Message):
    await message.answer("Пожалуйста, отправьте мне сообщение для перевода")


# Обработчик для текстовых сообщений
@dp.message(lambda message: message.content_type == 'text')
async def translate_text(message: Message):
    try:
        translated = translator.translate(message.text, src='auto', dest='en')
        await message.reply(translated.text)
    except Exception as e:
        await message.reply(f"Error: {e}")
        print(f"Ошибка при переводе: {message.text} - {e}")


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

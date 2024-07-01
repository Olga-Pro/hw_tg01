import asyncio
from aiogram import Bot, Dispatcher

from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import sqlite3

import os

from dotenv import load_dotenv
# Загрузка переменных окружения из файла .env
load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# Создание экземпляра бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

class Form(StatesGroup):
    name = State()
    age =State()
    grade = State()


def init_db():
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
    	CREATE TABLE IF NOT EXISTS students (
    	id INTEGER PRIMARY KEY AUTOINCREMENT,
    	name TEXT NOT NULL,
    	age INTEGER NOT NULL,
    	grade TEXT NOT NULL)
    	''')
    conn.commit()
    conn.close()


init_db()


# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(Form.name)

# Обработчик имени
@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)

# Обработчик возраста
@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("В каком классе ты учишься?")
    await state.set_state(Form.grade)

# Обработчик класса
@dp.message(Form.grade)
async def grade(message: Message, state: FSMContext):
    if message.text.startswith('/'):
        return  # Игнорируем команды
    await state.update_data(grade=message.text)
    user_data = await state.get_data()

    # Сохранение данных в базу данных
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
       INSERT INTO students (name, age, grade) VALUES (?, ?, ?)''',
                (user_data['name'], user_data['age'], user_data['grade']))
    conn.commit()
    conn.close()

    # Отправка сообщения с сохраненными данными
    await message.answer(f"Данные сохранены:\nИмя: {user_data['name']}\nВозраст: {user_data['age']}\nКласс: {user_data['grade']}")

    # Завершаем состояние
    await state.clear()

# Обработчик команды /base - вывести содержимое таблицы students
@dp.message(Command(commands=['base']))
async def show_base(message: Message):
    # Извлечение всех данных из базы данных
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('SELECT name, age, grade FROM students')
    rows = cur.fetchall()
    conn.close()

    # Формирование сообщения с данными
    if rows:
        response = "Список студентов:\n\n"
        for row in rows:
            response += f"Имя: {row[0]}, Возраст: {row[1]}, Класс: {row[2]}\n"
    else:
        response = "В базе данных нет студентов."

    # Отправка сообщения пользователю
    await message.answer(response)


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
